
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from Admin_App.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.utils.text import slugify
from Core.utils import OnlyAdminAccess
# Create your views here.

@csrf_exempt # this ajax request commming from add customer.html
def fetch_area(request):
    city_id=request.POST.get("city_id")
    area = Area.objects.filter(city = city_id ).order_by().values('area',str('id')).distinct()
    return JsonResponse(json.dumps(list(area), cls=DjangoJSONEncoder),content_type="application/json",safe=False)

@csrf_exempt # this ajax request commming from add customer.html
def fetch_service_price(request):
    service_id=request.POST.get("service_id")
    service = ServiceCateory.objects.get(id= service_id )
    data = {"price":[]}
    if service.is_payable:
        data = service.price
    return JsonResponse(data, content_type="application/json",safe=False)

@OnlyAdminAccess
def dashboard(request):
    user_count = Customer.objects.all().count()
    vender_count = Vender.objects.all().count()
    service_count = Service.objects.all().count()
    order_count = Order.objects.all().count()
    context = {
     "user_count":user_count, 
     "vender_count":vender_count, 
     "service_count":service_count,
     "order_count":order_count
    }
    return render(request, "admin_template/dashboard.html", context)

@OnlyAdminAccess
def service_category(request):
    if request.method =="POST":
        name = request.POST.get('name')
        image = request.FILES.get('image')
        is_payable = request.POST.get('is_payable')
        time = request.POST.getlist('time')
        price = request.POST.getlist('price')
        if name == "":
            messages.error(request,"Please Enter Category Name")
            return HttpResponseRedirect(reverse('admin_service_category')) 
        if image == None:
            messages.error(request,"Please Upload  Image")
            return HttpResponseRedirect(reverse('admin_service_category'))
        if ServiceCateory.objects.filter(name = name).exists():
            messages.error(request,f"Servvice Cateory {name} Already Exists")
            return HttpResponseRedirect(reverse('admin_service_category'))
        if is_payable == "True":
            timeprice= []
            for i in range(min([len(time), len(price)])):
                timeprice.append({"time":time[i],"price":price[i]})
            ServiceCateory.objects.create(name = name, image = image,is_payable = True, price={"price":timeprice}) 
        else:
            ServiceCateory.objects.create(name = name, image = image,is_payable = False,  price={"price":[]})
        messages.success(request,f"Service Cateory {name}")
        return HttpResponseRedirect(reverse('admin_service_category'))
    else:
        category = ServiceCateory.objects.all().order_by('name')
        context={
            "category":category
        }
        return render(request,'admin_template/service_category.html',context)

@OnlyAdminAccess
def update_service_category(request):
    if request.method =="POST":
        try:
            name = request.POST.get('name')
            service_id = request.POST.get('service_id')
            image = request.FILES.get('image')
            time = request.POST.getlist('time')
            price = request.POST.getlist('price')
            print(time)
            service_category = ServiceCateory.objects.filter(id = service_id).first()
            if name == "":
                messages.error(request,"Please Enter Category Name")
                return HttpResponseRedirect(reverse('admin_service_category')) 
            if ServiceCateory.objects.filter(name = name).exclude(name = service_category.name).exists():
                messages.error(request,f"Servvice Cateory {name} Already Exists")
                return HttpResponseRedirect(reverse('admin_service_category'))
            with transaction.atomic():
                service_category.name = name
                service_category.slug = slugify(name, allow_unicode=True)
                if service_category.is_payable:
                    timeprice= []
                    for i in range(min([len(time), len(price)])):
                        timeprice.append({"time":time[i],"price":price[i]})
                    service_category.price={"price":timeprice}
                else:
                    service_category.price={"price":[]}
                if image:
                    service_category.image = image
                service_category.save()
                messages.success(request,f"Service Cateory {name} Updated")
                return HttpResponseRedirect(reverse('admin_service_category'))
        except Exception as e:
            messages.error(request, f"Inernal Server Error {e}")
            return HttpResponseRedirect(reverse('admin_service_category'))
    else:
        messages.error(request, "Invalid Method ")
        return HttpResponseRedirect(reverse('admin_service_category'))

@OnlyAdminAccess
def vender(request):
    if request.method =="POST":
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        email= request.POST.get('email')
        phone= request.POST.get('phone')
        password= request.POST.get('password')
        alternative_phone= request.POST.get('alternative_phone')
        address= request.POST.get('address')
        pincode= request.POST.get('pincode')
        address_proof_type= request.POST.get('address_proof_type')
        address_proof_id= request.POST.get('address_proof_id')
        city = request.POST.get('city')
        area = request.POST.get('area')
        address_proof_photo = request.FILES.get('address_proof_photo')
        profile_photo = request.FILES.get('profile_photo')
        time = request.POST.getlist('time')
        service_category_id = request.POST.get('category')
        price = request.POST.getlist('price')
        if service_category_id and password and first_name and last_name and email and phone and alternative_phone and pincode and address and address_proof_type and address_proof_id and address_proof_photo and profile_photo and city and area:
            with transaction.atomic():
                user = CustomUser.objects.create_user(first_name = first_name,last_name=last_name,phone = phone,email=email,user_type = 2,password=password,is_active = True)
                user.vender.aletrnative_no = alternative_phone
                user.vender.account_active = True
                user.vender.pincode = pincode
                user.vender.address = address
                user.vender.city = City.objects.get(id = city)
                user.vender.area = Area.objects.get(id = area)
                user.vender.address_proof_type = address_proof_type
                user.vender.address_proof_id = address_proof_id
                user.vender.address_proof_photo = address_proof_photo
                user.vender.profile_photo = profile_photo
                user.save()
                service = ServiceCateory.objects.get(id = service_category_id)
                if service.is_payable:
                    timeprice= []
                    for i in range(min([len(time), len(price)])):
                        timeprice.append({"time":time[i],"price":price[i]})
                    Service.objects.create(vender = user.vender, category = service,is_payable = True, price={"price":timeprice}) 
                else:
                    Service.objects.create(vender = user.vender, category = service,is_payable = False,  price={"price":[]})
        else:
            messages.error(request,"Please Enter All The Filed")
            return HttpResponseRedirect(reverse('admin_vender')) 
        messages.success(request,f"Vender Added Successfully")
        return HttpResponseRedirect(reverse('admin_vender'))
    else:
        vender = Vender.objects.all().order_by('-created_at')
        category = ServiceCateory.objects.all().order_by('name')
        city = City.objects.all().order_by('city')
        service = Service.objects.all().order_by('-created_at')
        context={
            "category_list":category,
            "vender_list":vender,
            "city_list":city,
            "service_list":service
        }
        return render(request,'admin_template/vender.html',context)

@OnlyAdminAccess
def vender_details(request, id):
    if request.method =="POST":
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        email= request.POST.get('email')
        phone= request.POST.get('phone')
        password= request.POST.get('password')
        alternative_phone= request.POST.get('alternative_phone')
        address= request.POST.get('address')
        pincode= request.POST.get('pincode')
        address_proof_type= request.POST.get('address_proof_type')
        address_proof_id= request.POST.get('address_proof_id')
        city = request.POST.get('city')
        area = request.POST.get('area')
        address_proof_photo = request.FILES.get('address_proof_photo')
        profile_photo = request.FILES.get('profile_photo')
        time = request.POST.getlist('time')
        service_category_id = request.POST.get('category')
        price = request.POST.getlist('price')
        if service_category_id and first_name and last_name and email and phone and alternative_phone and pincode and address and address_proof_type and address_proof_id and address_proof_photo and profile_photo and city and area:
            with transaction.atomic():
                user = CustomUser.objects.create_user(first_name = first_name,last_name=last_name,phone = phone,email=email,user_type = 2,password=password,is_active = True)
                user.vender.aletrnative_no = alternative_phone
                user.vender.account_active = True
                user.vender.pincode = pincode
                user.vender.address = address
                user.vender.city = City.objects.get(id = city)
                user.vender.area = Area.objects.get(id = area)
                user.vender.address_proof_type = address_proof_type
                user.vender.address_proof_id = address_proof_id
                user.vender.address_proof_photo = address_proof_photo
                user.vender.profile_photo = profile_photo
                user.save()
                service = ServiceCateory.objects.get(id = service_category_id)
                if service.is_payable:
                    timeprice= []
                    for i in range(min([len(time), len(price)])):
                        timeprice.append({"time":time[i],"price":price[i]})
                    Service.objects.create(vender = user.vender, category = service,is_payable = True, price={"price":timeprice}) 
                else:
                    Service.objects.create(vender = user.vender, category = service,is_payable = False,  price={"price":[]})
        else:
            messages.error(request,"Please Enter All The Filed")
            return HttpResponseRedirect(reverse('admin_vender')) 
        messages.success(request,f"Vender Added Successfully")
        return HttpResponseRedirect(reverse('admin_vender'))
    else:
        try:
            service_list = Service.objects.filter(vender = id).select_related('category', 'vender')
            context={
            "vender_details":Vender.objects.get(id=id),
            "service_list":service_list,
            "category_list":ServiceCateory.objects.all().order_by('name'),
            "city_list":City.objects.all().order_by('city'),
            "area_list":Area.objects.all().order_by('area'),
            "order_list":Order.objects.filter(service__in = service_list.values('id')).order_by('-created_at')
            }
            return render(request,'admin_template/vender_details.html',context)
        except Exception as e:
            print(e)
            messages.error(request,"Vender Not Found")
            return HttpResponseRedirect(reverse('admin_vender'))


@OnlyAdminAccess
def customer(request):
    customer = Customer.objects.all().order_by('-created_at')
    context={
        "customer_list":customer
    }
    return render(request,'admin_template/customer.html',context)

@OnlyAdminAccess
def customer_details(request, id):
    try:
        customer_details = Customer.objects.get(id=id)
        context={
        "customer_details":customer_details,
        "order_list":Order.objects.filter(customer = id).order_by('-created_at').select_related('customer', 'service')
        }
        return render(request,'admin_template/customer_details.html',context)
    except Exception as e:
        print(e)
        messages.error(request,"Vender Not Found")
        return HttpResponseRedirect(reverse('admin_vender'))


@OnlyAdminAccess
def order(request):
    order = Order.objects.all().order_by('status','-created_at')
    context={
        "order_list":order
    }
    return render(request,'admin_template/order.html',context)

@OnlyAdminAccess
def order_details(request, id):
    try:
        order_details = Order.objects.get(id=id)
        context={
        "order_details":order_details,
        }
        return render(request,'admin_template/order_details.html',context)
    except Exception as e:
        print(e)
        messages.error(request,"Vender Not Found")
        return HttpResponseRedirect(reverse('admin_vender'))


@OnlyAdminAccess
def update_vender_profile(request, id):
    if request.method =="POST":
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        email= request.POST.get('email')
        phone= request.POST.get('phone')
        password= request.POST.get('password')
        alternative_phone= request.POST.get('alternative_phone')
        address= request.POST.get('address')
        pincode= request.POST.get('pincode')
        city = request.POST.get('city')
        area = request.POST.get('area')
        profile_photo = request.FILES.get('profile_photo')
        if first_name and last_name and email and phone and alternative_phone and pincode and address and city and area:
            with transaction.atomic():
                vender = Vender.objects.get(id = id)
                vender.aletrnative_no = alternative_phone
                vender.pincode = pincode
                vender.address = address
                vender.city = City.objects.get(id = city)
                vender.area = Area.objects.get(id = area)
                if profile_photo:
                    vender.profile_photo = profile_photo
                vender.save()
                user = CustomUser.objects.get(id = vender.cu.id)
                user.first_name = first_name
                user.last_name = last_name
                user.email= email
                user.phone = phone
                if password :
                    user.set_password(password)
                user.save()
                messages.success(request,f"Vender Profile Updated Successfully")
                return HttpResponseRedirect(reverse('admin_vender_details', kwargs={"id":id})) 
        else:
            messages.error(request,"Please Enter All The Filed")
            return HttpResponseRedirect(reverse('admin_vender_details', kwargs={"id":id})) 
    else:
        messages.error(request,"Method Must Be POST")
        return HttpResponseRedirect(reverse('admin_vender_details', kwargs={"id":id})) 

@OnlyAdminAccess
def update_service_price(request, id):
    if request.method =="POST":
        time = request.POST.getlist('time')
        service_id = request.POST.get('service_id')
        price = request.POST.getlist('price')
        if service_id and len(time) == len(price):
            with transaction.atomic():
                service = Service.objects.get(id = service_id)
                if service.is_payable:
                    timeprice= []
                    for i in range(min([len(time), len(price)])):
                        timeprice.append({"time":time[i],"price":price[i]})
                    service.price={"price":timeprice} 
                    service.save()
                    messages.success(request,"Service Price Updtaed")
                    return HttpResponseRedirect(reverse('admin_vender_details', kwargs={"id":id}))
                else:
                    messages.error(request,"Service is not payable")
                    return HttpResponseRedirect(reverse('admin_vender_details', kwargs={"id":id}))
        else:
            messages.error(request,"Please Enter All The Filed")
            return HttpResponseRedirect(reverse('admin_vender_details', kwargs={"id":id})) 
    else:
        messages.error(request,"Method Must Be POST")
        return HttpResponseRedirect(reverse('admin_vender_details', kwargs={"id":id})) 

@OnlyAdminAccess
def city(request):
    if request.method =="POST":
        name = request.POST.get('name')
        if name == "":
            messages.error(request,"Please Enter City Name")
            return HttpResponseRedirect(reverse('admin_city')) 
        if name == None:
            messages.error(request,"Please Upload  Image")
            return HttpResponseRedirect(reverse('admin_city'))
        if City.objects.filter(city = name).exists():
            messages.error(request,f"City {name} Already Exists")
            return HttpResponseRedirect(reverse('admin_city'))
        City.objects.create(city = name)
        messages.success(request,f"New City Created {name}")
        return HttpResponseRedirect(reverse('admin_city'))
    else:
        city = City.objects.all().order_by('city')
        context={
            "city_list":city,
        }
        return render(request,'admin_template/city.html',context)

@OnlyAdminAccess
def area(request):
    if request.method =="POST":
        name = request.POST.get('name')
        city = request.POST.get('city')
        if name == "":
            messages.error(request,"Please Enter Area Name")
            return HttpResponseRedirect(reverse('admin_area')) 
        if city == None:
            messages.error(request,"Please Select Category")
            return HttpResponseRedirect(reverse('admin_area'))
        if Area.objects.filter(area = name, city = city).exists():
            messages.error(request,f"Area {name} Already Exists")
            return HttpResponseRedirect(reverse('admin_area'))
        Area.objects.create(area = name, city = City.objects.get(id = city))
        messages.success(request,f"Service Area created {name}")
        return HttpResponseRedirect(reverse('admin_area'))
    else:
        city = City.objects.all().order_by('city')
        area = Area.objects.all().order_by('city__city')
        context={
            "city_list":city,
            "area_list":area
        }
        return render(request,'admin_template/area.html',context)

@OnlyAdminAccess
def admin_profile(request):
    if request.method =="POST":
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        if first_name and last_name :
            with transaction.atomic():
                user = CustomUser.objects.get(id = request.user.id)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                messages.success(request,f"Admin Profile Updated Successfully")
                return HttpResponseRedirect(reverse('admin_profile')) 
        else:
            messages.error(request,"Please Enter All The Filed")
            return HttpResponseRedirect(reverse('admin_profile')) 
    else:
        try:
            return render(request,'admin_template/profile.html')
        except Exception as e:
            messages.error(request,e)
            return HttpResponseRedirect(reverse('admin_dashboard'))

@OnlyAdminAccess
def admin_update_password(request):
    if request.method =="POST":
        current_password= request.POST.get('current_password')
        new_password= request.POST.get('new_password')
        new_confirm_password= request.POST.get('new_confirm_password')
        if current_password and new_password  and new_confirm_password :
            if new_password != new_confirm_password:
                messages.error(request,"New Confirm Password Mismatch")
                return HttpResponseRedirect(reverse('admin_profile')) 
            with transaction.atomic():
                user = CustomUser.objects.get(id = request.user.id)
                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()
                    messages.success(request,f"Password Updated Successfully")
                    return HttpResponseRedirect(reverse('logout')) 
                else:
                    messages.error(request,"Incorrect Current Password")
                    return HttpResponseRedirect(reverse('admin_profile'))
        else:
            messages.error(request,"Please Enter All The Filed")
            return HttpResponseRedirect(reverse('admin_profile')) 
    else:
        messages.error(request, "Invalid Method GET")
        return HttpResponseRedirect(reverse('admin_profile'))
