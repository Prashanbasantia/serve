from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from Admin_App.models import *
from django.db import  transaction
import random
from Core.utils import semd_register_otp_email
from django.conf import settings
from Admin_App.AuthBackend import Login
from django.contrib.auth import  login as log_in, logout as log_out
from Core.utils import OnlyUserAccess
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum,Q,Count,F
from django.db.models.functions import Coalesce,Cast
# Create your views here.

def home(request):
    service_category  = ServiceCateory.objects.all().order_by("-created_at")
    popular_vender  = Vender.objects.all().order_by("?"[:10])
    context={
        "service_category_list": service_category,
        "popular_vender": popular_vender
    }
    return render(request, "index_template/index.html", context)
    
def login(request):
    log_user = request.user
    if log_user.is_authenticated and log_user.user_type == "3":
        return HttpResponseRedirect(reverse("account"))
    if log_user.is_authenticated and log_user.user_type == "1":
        return HttpResponseRedirect(reverse('admin_dashboard'))
    if log_user.is_authenticated and log_user.user_type == "2":
        return HttpResponseRedirect(reverse('vender_dashboard'))
    if request.method == "POST":
        user=Login.authenticate(request,email=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            if user.is_active==True:
                log_in(request,user)
                try:
                    if user.user_type=="1" :
                        return HttpResponseRedirect(reverse('dashboard'))
                    elif user.user_type=="3":
                        return HttpResponseRedirect(reverse("account"))
                    else:
                        return HttpResponseRedirect(reverse('login'))
                except Exception as e:
                    return HttpResponseRedirect(reverse('login'))
            else:
                messages.error(request,"Your Account Is Disable ! Contact Us")
                return HttpResponseRedirect(reverse('login'))
        else:
            messages.error(request,"Invalid Email or Password")
            return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, "index_template/login.html")

def create_user_account(request):
    if request.method == "POST":
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        email_otp = request.POST.get('email_otp')
        phone_otp = request.POST.get('phone_otp')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        if not email and not phone and not first_name and not last_name and not email_otp and not phone_otp:
            messages.error(request,"Fill All The Field")
            return HttpResponseRedirect(reverse('signup'))
        get_email_opt = EmailOtp.objects.filter(email=email).order_by('-created_at')
        get_phone_opt = PhoneOtp.objects.filter(phone=phone).order_by('-created_at')
        print(get_email_opt, get_phone_opt, email, phone, last_name, first_name, email_otp, phone_otp)
        if not get_email_opt:
            messages.error(request,"Invalid Email")
            return HttpResponseRedirect(reverse('signup'))
        if not get_phone_opt:
            messages.error(request,"Invalid Phone Number")
            return HttpResponseRedirect(reverse('signup'))
        if str(get_email_opt.first().otp) != str(email_otp) :
            messages.error(request,"Invalid Email OTP")
            return HttpResponseRedirect(reverse('signup'))
        if  str(get_phone_opt.first().otp) != str(phone_otp):
            messages.error(request,"Invalid Phone OTP")
            return HttpResponseRedirect(reverse('signup'))
        with transaction.atomic():
            user = CustomUser.objects.create_user(first_name = first_name,last_name=last_name,phone = phone,email=email,user_type = 3,password=password,is_active = True)
            user.customer.pincode = pincode
            user.customer.address = address
            user.customer.city = "bhubaneswar"
            user.customer.address = "Odisha"
            user.save()
            messages.success(request,"Account Created Successfully")
            return HttpResponseRedirect(reverse('signup'))
    else:
        messages.error(request,"Request Must Be POST ")
        return HttpResponseRedirect(reverse('signup'))

def signup(request):
    if request.method == "POST":
        try:
            first_name = request.POST["fname"]
            last_name = request.POST["lname"]
            email = request.POST["email"]
            phone = request.POST["phone"] 
            password = request.POST["password"]
            pincode = request.POST["pincode"]
            address = request.POST["address"]
            if not email and not phone  and not first_name and not last_name and not pincode and not address:
                messages.error(request,"Fill All The Required Field")
                return HttpResponseRedirect(reverse('signup'))
            if not len(first_name) >=3 and  first_name.isalpha():
                messages.error(request,"First Name must be greater than 2 chars and Also Alphabets")
                return HttpResponseRedirect(reverse('signup'))
            if not len(last_name) >=3 and  last_name.isalpha():
                messages.error(request,"Last Name must be greater than 2 chars and Also Alphabets")
                return HttpResponseRedirect(reverse('signup'))
            if CustomUser.objects.filter(email = email).exists():
                messages.error(request,"Email is already exists . User another one")
                return HttpResponseRedirect(reverse('signup'))
            if CustomUser.objects.filter(phone = phone).exists():
                messages.error(request,"Phone Number is already exists . User another one")
                return HttpResponseRedirect(reverse('signup'))
            email_otp = "123456" #random.randint(100000,999999)
            phone_otp = email_otp
            EmailOtp.objects.create(email = email ,otp = email_otp)
            PhoneOtp.objects.create(phone=phone ,otp = phone_otp)
            if settings.DEBUG:
                print("email opt",email_otp, "phone otp", phone_otp)
            else:
                print("email opt",email_otp, "phone otp", phone_otp)
                #semd_register_otp_email(email,email_otp)#call this function from utils.py file to send otp to email
            context = {
                'first_name':first_name,
                'last_name':last_name,
                'email':email,
                'phone':phone,
                'password':password,
                'pincode':pincode,
                'address':address
                    }
            return render(request, "index_template/user_signup_otp.html", context)
        except Exception as e:
            print("error", e)
            messages.error(request,"Something Went Wrong")
            return HttpResponseRedirect(reverse('signup'))
    else:
        return render(request, "index_template/signup.html")

def signup_vender(request):
    context={
        "city_list":City.objects.all().order_by('city')
    }
    return render(request, "index_template/signup_vender.html", context)

@csrf_exempt
def verify_signup_vender(request):
    if request.method == "POST":
        try:
            first_name = request.POST["fname"]
            last_name = request.POST["lname"]
            email = request.POST["email"]
            phone = request.POST["phone"] 
            alternative_phone = request.POST["phone"] 
            password = request.POST["password"]
            city = request.POST["city"]
            area = request.POST["area"]
            pincode = request.POST["pincode"]
            address = request.POST["address"]
            id_proof = request.POST["id_proof"]
            id_proof_no = request.POST["id_proof_no"]
            area = request.POST["area"]
            id_proof_photo = request.FILES["id_proof_photo"]
            profile_photo = request.FILES["profile_photo"]
            if not email and not phone and not password  and not first_name and not last_name and not pincode and not address and not alternative_phone and not city and not area and not id_proof and not id_proof_no and not id_proof_photo and not profile_photo:
                data = {
                "success":False,
                "message":"Fill All The Field"
                }
                return JsonResponse(data,content_type="application/json",safe=False)
            if not len(first_name) >=3 and  first_name.isalpha():
                data = {
                "success":False,
                "message":"First Name must be greater than 2 chars and Also Alphabets"
                }
                return JsonResponse(data,content_type="application/json",safe=False)
            if not len(last_name) >=3 and  last_name.isalpha():
                data = {
                "success":False,
                "message":"Last Name must be greater than 2 chars and Also Alphabets"
                }
                return JsonResponse(data,content_type="application/json",safe=False)
            if CustomUser.objects.filter(email = email).exists():
                data = {
                "success":False,
                "message":"Email is already exists . User another one"
                }
                return JsonResponse(data,content_type="application/json",safe=False)
            if CustomUser.objects.filter(phone = phone).exists():
                data = {
                "success":False,
                "message":"Phone Number is already exists . User another one"
                }
                return JsonResponse(data,content_type="application/json",safe=False)
            email_otp = "123456" #random.randint(100000,999999)
            phone_otp = email_otp
            EmailOtp.objects.create(email = email ,otp = email_otp)
            PhoneOtp.objects.create(phone=phone ,otp = phone_otp)
            if settings.DEBUG:
                print("email opt",email_otp, "phone otp", phone_otp)
            else:
                print("email opt",email_otp, "phone otp", phone_otp)
                #semd_register_otp_email(email,email_otp)#call this function from utils.py file to send otp to email
            data = {
                "success":True,
                "message":"An OTP Send To Your Mobile No"
                }
            return JsonResponse(data,content_type="application/json",safe=False)
        except Exception as e:
            print("error", e)
            data = {
            "success":False,
            "message":"Internal Server Error"
            }
            return JsonResponse(data,content_type="application/json",safe=False)
    else:
        data = {
            "success":False,
            "message":"Method Most be POST"
        }
        return JsonResponse(data,content_type="application/json",safe=False)

@csrf_exempt
def create_vender_account(request):
    if request.method == "POST":
        try:
            print(request.POST)
            first_name = request.POST["fname"]
            last_name = request.POST["lname"]
            email = request.POST["email"]
            phone = request.POST["phone"] 
            alternative_phone = request.POST["phone"] 
            password = request.POST["password"]
            city = request.POST["city"]
            area = request.POST["area"]
            pincode = request.POST["pincode"]
            address = request.POST["address"]
            id_proof = request.POST["id_proof"]
            id_proof_no = request.POST["id_proof_no"]
            area = request.POST["area"]
            phone_otp = request.POST["phone_otp"]
            id_proof_photo = request.FILES["id_proof_photo"]
            profile_photo = request.FILES["profile_photo"]
            if not email and not phone and not password  and not first_name and not last_name and not pincode and not address and not alternative_phone and not city and not area and not id_proof and not id_proof_no and not id_proof_photo and not profile_photo:
                data = {
                "success":False,
                "message":"Fill All The Field"
                }
                return JsonResponse(data,content_type="application/json",safe=False)
            if not len(first_name) >=3 and  first_name.isalpha():
                data = {
                "success":False,
                "message":"First Name must be greater than 2 chars and Also Alphabets"
                }
                return JsonResponse(data,content_type="application/json",safe=False)
            if not len(last_name) >=3 and  last_name.isalpha():
                data = {
                "success":False,
                "message":"Last Name must be greater than 2 chars and Also Alphabets"
                }
                return JsonResponse(data,content_type="application/json",safe=False)
            if CustomUser.objects.filter(email = email).exists():
                data = {
                "success":False,
                "message":"Email is already exists . User another one"
                }
                return JsonResponse(data,content_type="application/json",safe=False)
            if CustomUser.objects.filter(phone = phone).exists():
                data = {
                "success":False,
                "message":"Phone Number is already exists . User another one"
                }
                return JsonResponse(data,content_type="application/json",safe=False)
            
            get_phone_opt = PhoneOtp.objects.filter(phone=phone).order_by('-created_at')
            if not get_phone_opt:
                data = {
                "success":False,
                "message":"Invalid Phone Number"
                }
                return JsonResponse(data,content_type="application/json",safe=False)
            if  str(get_phone_opt.first().otp) != str(phone_otp):
                data = {
                "success":False,
                "message":"Invalid OTP"
                }
                return JsonResponse(data,content_type="application/json",safe=False)
            with transaction.atomic():
                user = CustomUser.objects.create_user(first_name = first_name,last_name=last_name,phone = phone,email=email,user_type = 2,password=password,is_active = True)
                user.vender.pincode = pincode
                user.vender.address = address
                user.vender.aletrnative_no = alternative_phone
                user.vender.city = City.objects.get(id = city)
                user.vender.area = Area.objects.get(id = area)
                user.vender.address_proof_type = id_proof
                user.vender.address_proof_id = id_proof_no
                user.vender.address_proof_photo = id_proof_photo
                user.vender.profile_photo = profile_photo
                user.save()  
                data = {
                    "success":True,
                    "message":"Account Created Successfully"
                    }
                return JsonResponse(data,content_type="application/json",safe=False)
        except Exception as e:
            print("error", e)
            data = {
            "success":False,
            "message":"Internal Server Error"
            }
            return JsonResponse(data,content_type="application/json",safe=False)
    else:
        data = {
            "success":False,
            "message":"Method Most be POST"
        }
        return JsonResponse(data,content_type="application/json",safe=False)

def aboutus(request):
    return render(request, "index_template/about.html")

def contactus(request):
    return render(request, "index_template/contact.html")

def service(request):
    city_name = request.GET.get('city')
    area_name = request.GET.get('area')
    category_name = request.GET.get('category')
    if city_name and area_name and category_name:
        category  = ServiceCateory.objects.all().order_by("name")
        city_list  = City.objects.all().order_by("city")
        area_list  = Area.objects.filter(city__city = city_name).order_by("area")
        vender_list = Vender.objects.filter(city__city = city_name, area__area = area_name).values('id')
        service  = Service.objects.filter(category__name = category_name, vender__in = vender_list).order_by("?")
    elif not city_name and not area_name and category_name:
        category  = ServiceCateory.objects.all().order_by("name")
        city_list  = City.objects.all().order_by("city")
        area_list  = Area.objects.all().order_by("area")
        service  = Service.objects.filter(category__name = category_name).order_by("?")[:20]
    else:
        category  = ServiceCateory.objects.all().order_by("-created_at")
        city_list  = City.objects.all().order_by("city")
        area_list  = Area.objects.all().order_by("-area")
        service  = Service.objects.all().order_by("?")[:10]
    context={
        "service_list": service,
        "city_list": city_list,
        "area_list": area_list,
        "category_list": category,
        "city_name":city_name,
        "area_name":area_name,
        "category_name":category_name
    }
    return render(request, "index_template/service.html", context)

def service_details(request, id):
    service  = Service.objects.get(id = id)
    context={
        "service_list": service,
    }
    return render(request, "index_template/service_details.html", context)

def faq(request):
    return render(request, "index_template/faq.html")

def logout(request):
    log_out(request)
    return HttpResponseRedirect(reverse('login'))
 
#   all auth url

@OnlyUserAccess
def account(request):
    order_recent = Order.objects.filter(customer = request.user.customer.id).order_by('status','-created_at').first()
    order_count =Order.objects.aggregate(
                    order_running=Count('id',filter=Q(status = 1)),
                    order_pending=Count('id',filter=Q(status = 2)),
                    order_complete=Count('id',filter=Q(status = 3)),
                    order_cancelled=Count('id',filter=Q(status = 4)),
                        )

    context = {
        "order_recent":order_recent,
        "order_complete":order_count['order_running'] + order_count['order_complete'],
        "order_pending":order_count['order_pending'],
        "order_cancelled":order_count['order_cancelled'],
        "order_total":order_count['order_running'] + order_count['order_complete']+order_count['order_cancelled']+order_count['order_pending']
    }
    return render(request, "index_template/account.html", context)

@OnlyUserAccess
def orders(request):
    order_list = Order.objects.filter(customer = request.user.customer.id).order_by('status','-created_at')
    context = {
        "order_list":order_list
    }
    return render(request, "index_template/account.html", context)

@OnlyUserAccess
def profile(request):
    return render(request, "index_template/account.html")

@OnlyUserAccess
def session_clear(request):
    return render(request, "index_template/account.html")


@OnlyUserAccess
def service_order(request, id):
    if request.method == "POST":
        service  = Service.objects.get(id = id)
        amount = request.POST.get('price')
        if service.is_payable:
            order = Order(is_payable = True,day_price = amount, service = service, customer = request.user.customer)
            order.save()
        else:
            order = Order(day_price = amount, service = service, customer = request.user.customer)
            order.save()
        return HttpResponseRedirect(reverse('service_order_info', kwargs={"id":order.id}))
    else:
        service  = Service.objects.get(id = id)
        context={
            "service_list": service,
        }
        return render(request, "index_template/order.html", context)

@OnlyUserAccess
def service_order_info(request, id):
    order  = Order.objects.get(id = id)
    context={
        "order_info": order,
    }
    return render(request, "index_template/order_info.html", context)

@OnlyUserAccess
def change_password(request):
    if request.method =="POST":
        current_password= request.POST.get('current_password')
        new_password= request.POST.get('new_password')
        new_confirm_password= request.POST.get('new_confirm_password')
        if current_password and new_password  and new_confirm_password :
            if new_password != new_confirm_password:
                messages.error(request,"New Confirm Password Mismatch")
                return HttpResponseRedirect(reverse('profile')) 
            with transaction.atomic():
                user = CustomUser.objects.get(id = request.user.id)
                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()
                    messages.success(request,f"Password Updated Successfully")
                    return HttpResponseRedirect(reverse('logout')) 
                else:
                    messages.error(request,"Incorrect Current Password")
                    return HttpResponseRedirect(reverse('profile'))
        else:
            messages.error(request,"Please Enter All The Filed")
            return HttpResponseRedirect(reverse('profile')) 
    else:
        messages.error(request, "Invalid Method GET")
        return HttpResponseRedirect(reverse('profile'))

@OnlyUserAccess
def change_address(request):
    if request.method =="POST":
        address= request.POST.get('address')
        pincode= request.POST.get('pincode')
        if address and pincode :
            with transaction.atomic():
                user = Customer.objects.get(id = request.user.customer.id)
                user.address = address
                user.pincode = pincode
                user.save()
                messages.success(request,f"Address Updated Successfully")
                return HttpResponseRedirect(reverse('profile')) 
        else:
            messages.error(request,"Please Enter All The Filed")
            return HttpResponseRedirect(reverse('profile')) 
    else:
        messages.error(request, "Invalid Method GET")
        return HttpResponseRedirect(reverse('profile'))
