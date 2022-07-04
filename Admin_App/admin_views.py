import email
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from Admin_App.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
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
def dashboard(request):
    return render(request, "admin_template/dashboard.html")
    
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
        if name == None:
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

def service(request):
    if request.method =="POST":
        name = request.POST.get('name')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        if name == "":
            messages.error(request,"Please Enter Category Name")
            return HttpResponseRedirect(reverse('service_category')) 
        if name == None:
            messages.error(request,"Please Upload  Image")
            return HttpResponseRedirect(reverse('admin_service'))
        if category == None:
            messages.error(request,"Please Select Category")
            return HttpResponseRedirect(reverse('admin_service'))
        if Service.objects.filter(name = name).exists():
            messages.error(request,f"Servvice {name} Already Exists")
            return HttpResponseRedirect(reverse('admin_service'))
        Service.objects.create(name = name, image = image, category = ServiceCateory.objects.get(id = category))
        messages.success(request,f"Service Cateory {name}")
        return HttpResponseRedirect(reverse('admin_service'))
    else:
        vender = Vender.objects.all().order_by('-created_at')
        category = ServiceCateory.objects.all().order_by('name')
        service = Service.objects.all().order_by('-created_at')
        context={
            "category_list":category,
            "vender_list":vender,
            "service_list":service
        }
        return render(request,'admin_template/service.html',context)

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
        print(service_category_id, first_name, last_name, email, phone, alternative_phone, pincode, address, address_proof_type, address_proof_id, address_proof_photo, profile_photo, city, area)
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
        print(service)
        context={
            "city_list":city,
        }
        return render(request,'admin_template/city.html',context)


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
        print(service)
        context={
            "city_list":city,
            "area_list":area
        }
        return render(request,'admin_template/area.html',context)