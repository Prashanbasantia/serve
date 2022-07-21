
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from Admin_App.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import transaction
from django.utils.text import slugify
from Core.utils import OnlyVenderAccess
# Create your views here.
@OnlyVenderAccess
def vender_dashboard(request):
    service_count = Service.objects.filter(vender = request.user.vender.id).count()
    order_count = Order.objects.filter(service__vender = request.user.vender.id)
    user_count = Customer.objects.filter(id__in = order_count.values('customer')).distinct().count()
    context = {
     "user_count":user_count, 
     "service_count":service_count,
     "order_count":order_count.count()
    }
    return render(request, "vender_template/dashboard.html", context)

@OnlyVenderAccess
def vender_service(request):
    if request.method =="POST":
        time = request.POST.getlist('time')
        service_category_id = request.POST.get('category')
        price = request.POST.getlist('price')
        if service_category_id:
            with transaction.atomic():
                service = ServiceCateory.objects.get(id = service_category_id)
                if Service.objects.filter(vender = request.user.vender.id, category = service_category_id).exists():
                    messages.error(request,"Service Already Exists")
                    return HttpResponseRedirect(reverse('vender_service'))
                if service.is_payable:
                    timeprice= []
                    for i in range(min([len(time), len(price)])):
                        timeprice.append({"time":time[i],"price":price[i]})
                    Service.objects.create(vender = request.user.vender, category = service,is_payable = True, price={"price":timeprice}) 
                else:
                    Service.objects.create(vender = request.user.vender, category = service,is_payable = False,  price={"price":[]})

                messages.success(request,f"Service Added Successfully")
                return HttpResponseRedirect(reverse('vender_service'))
        else:
            messages.error(request,"Please Select any service")
            return HttpResponseRedirect(reverse('vender_service')) 
    else:
        try:
            service_list = Service.objects.filter(vender = request.user.vender.id).select_related('category', 'vender')
            context={
            "service_list":service_list,
            "category_list":ServiceCateory.objects.all().exclude(id__in = service_list.values('category')).order_by('name')
            }
            return render(request,'vender_template/service_details.html',context)
        except Exception as e:
            messages.error(request,e)
            return HttpResponseRedirect(reverse('vender_dashboard'))

@OnlyVenderAccess
def update_service_price(request):
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
                    return HttpResponseRedirect(reverse('vender_service'))
                else:
                    messages.error(request,"Service is not payable")
                    return HttpResponseRedirect(reverse('vender_service'))
        else:
            messages.error(request,"Please Enter All The Filed")
            return HttpResponseRedirect(reverse('vender_service')) 
    else:
        messages.error(request,"Method Must Be POST")
        return HttpResponseRedirect(reverse('vender_service')) 


@OnlyVenderAccess
def vender_profile(request):
    if request.method =="POST":
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        alternative_phone= request.POST.get('alternative_phone')
        address= request.POST.get('address')
        pincode= request.POST.get('pincode')
        city = request.POST.get('city')
        area = request.POST.get('area')
        profile_photo = request.FILES.get('profile_photo')
        if first_name and last_name  and alternative_phone and pincode and address and city and area:
            with transaction.atomic():
                vender = request.user.vender
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
                user.save()
                messages.success(request,f"Vender Profile Updated Successfully")
                return HttpResponseRedirect(reverse('vender_profile')) 
        else:
            messages.error(request,"Please Enter All The Filed")
            return HttpResponseRedirect(reverse('vender_profile')) 
    else:
        try:
            context={
            "city_list":City.objects.all().order_by('city'),
            "area_list":Area.objects.all().order_by('area'),
            }
            return render(request,'vender_template/profile.html',context)
        except Exception as e:
            messages.error(request,e)
            return HttpResponseRedirect(reverse('vender_dashboard'))

@OnlyVenderAccess
def vender_update_password(request):
    if request.method =="POST":
        current_password= request.POST.get('current_password')
        new_password= request.POST.get('new_password')
        new_confirm_password= request.POST.get('new_confirm_password')
        if current_password and new_password  and new_confirm_password :
            if new_password != new_confirm_password:
                messages.error(request,"New Confirm Password Mismatch")
                return HttpResponseRedirect(reverse('vender_profile')) 
            with transaction.atomic():
                user = CustomUser.objects.get(id = request.user.id)
                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()
                    messages.success(request,f"Password Updated Successfully")
                    return HttpResponseRedirect(reverse('logout')) 
                else:
                    messages.error(request,"Incorrect Current Password")
                    return HttpResponseRedirect(reverse('vender_profile'))
        else:
            messages.error(request,"Please Enter All The Filed")
            return HttpResponseRedirect(reverse('vender_profile')) 
    else:
        messages.error(request, "Invalid Method GET")
        return HttpResponseRedirect(reverse('vender_profile'))

@OnlyVenderAccess
def order(request):
    order = Order.objects.filter(service__vender = request.user.vender.id).order_by('status','-created_at')
    context={
        "order_list":order
    }
    return render(request,'vender_template/order.html',context)