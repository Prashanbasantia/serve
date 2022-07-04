from logging import exception
from shutil import ExecError
from unicodedata import category
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
# Create your views here.

def home(request):
    service_category  = ServiceCateory.objects.all().order_by("-created_at")
    context={
        "service_category_list": service_category
    }
    return render(request, "index_template/index.html", context)
    
def login(request):
    log_user = request.user
    if log_user.is_authenticated and log_user.user_type == "3":
        return HttpResponseRedirect(reverse("account"))
    elif log_user.is_authenticated and log_user.user_type == "1":
        return HttpResponseRedirect(reverse('dashboard'))
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
                semd_register_otp_email(email,email_otp)#call this function from utils.py file to send otp to email
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

def aboutus(request):
    return render(request, "index_template/about.html")

def account(request):
    return render(request, "index_template/account.html")
    
def contactus(request):
    return render(request, "index_template/contact.html")

def service(request):
    category  = ServiceCateory.objects.all().order_by("-created_at")
    city_list  = City.objects.all().order_by("city")
    area_list  = Area.objects.all().order_by("-area")
    service  = Service.objects.all().order_by("-created_at")
    context={
        "service_list": service,
        "city_list": city_list,
        "area_list": area_list,
        "category_list": category
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

def pricing(request):
    return render(request, "index_template/pricing.html")

def logout(request):
    log_out(request)
    return HttpResponseRedirect(reverse('login'))

