from datetime import datetime, timedelta
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid 
from .ModelManager import CustomUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

class City(models.Model):
    id=models.UUIDField(editable=False,primary_key=True)
    city = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = uuid.uuid4()
            while City.objects.filter(id=self.id).exists():
                self.id = uuid.uuid4()
        super(City,self).save()

class Area(models.Model):
    id=models.UUIDField(editable=False,primary_key=True)
    city=models.ForeignKey(City,on_delete=models.CASCADE)
    area = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = uuid.uuid4()
            while Area.objects.filter(id=self.id).exists():
                self.id = uuid.uuid4()
        super(Area,self).save()

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id=models.UUIDField(editable=False,primary_key=True)
    user_type_data=((1,"Admin"),(2,"Vendor"),(3,"Customer"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=1)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    coin = models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone','first_name','last_name']
    objects = CustomUserManager()
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = uuid.uuid4()
            while CustomUser.objects.filter(id=self.id).exists():
                self.id = uuid.uuid4()
        super(CustomUser,self).save()

class Admin(models.Model):
    id=models.UUIDField(editable=False,primary_key=True)
    cu=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = uuid.uuid4()
            while Admin.objects.filter(id=self.id).exists():
                self.id = uuid.uuid4()
        super(Admin,self).save()

class Vender(models.Model):
    id=models.UUIDField(editable=False,primary_key=True)
    profile_photo = models.ImageField(upload_to="profile_photo/")
    cu=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    pincode = models.CharField(max_length=6)
    city=models.ForeignKey(City,on_delete=models.CASCADE)
    area=models.ForeignKey(Area,on_delete=models.CASCADE)
    address = models.TextField()
    account_active = models.BooleanField(default=False)
    aletrnative_no = models.CharField(max_length=10)
    address_proof_type = models.CharField(max_length=255)
    address_proof_id = models.CharField(max_length=255)
    address_proof_photo = models.ImageField(upload_to="address_proof/")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = uuid.uuid4()
            while Vender.objects.filter(id=self.id).exists():
                self.id = uuid.uuid4()
        super(Vender,self).save()
    
class Customer(models.Model):
    id=models.UUIDField(editable=False,primary_key=True)
    cu=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    pincode = models.CharField(max_length=6)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    address = models.TextField()
    account_active = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = uuid.uuid4()
            while Customer.objects.filter(id=self.id).exists():
                self.id = uuid.uuid4()
        super(Customer,self).save()

class PhoneOtp(models.Model):
    id=models.UUIDField(editable=False,primary_key=True)
    phone = models.CharField(max_length=10)
    otp = models.IntegerField()
    is_expire = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = uuid.uuid4()
            while PhoneOtp.objects.filter(id=self.id).exists():
                self.id = uuid.uuid4()
        super(PhoneOtp,self).save()

class EmailOtp(models.Model):
    id=models.UUIDField(editable=False,primary_key=True)
    email = models.EmailField(_('email address'))
    otp = models.IntegerField()
    is_expire = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = uuid.uuid4()
            while EmailOtp.objects.filter(id=self.id).exists():
                self.id = uuid.uuid4()
        super(EmailOtp,self).save()

class ServiceCateory(models.Model):
    id=models.UUIDField(editable=False,primary_key=True)
    slug = models.SlugField(unique=True)
    is_payable = models.BooleanField(default=False)
    price = models.JSONField(blank = True)
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="category/")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = uuid.uuid4()
            while ServiceCateory.objects.filter(id=self.id).exists():
                self.id = uuid.uuid4()
            self.slug = slugify(self.name, allow_unicode=True)
        super(ServiceCateory,self).save()

class Service(models.Model):
    id=models.UUIDField(editable=False,primary_key=True)
    category = models.ForeignKey(ServiceCateory, on_delete=models.CASCADE)
    vender = models.ForeignKey(Vender, on_delete=models.CASCADE)
    is_payable = models.BooleanField(default=False)
    price = models.JSONField(blank = True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
            while Service.objects.filter(id=self.id).exists():
                self.id = uuid.uuid4()
        super(Service, self).save()

class Order(models.Model):
    id=models.UUIDField(editable=False,primary_key=True)
    slug = models.SlugField(unique=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vender = models.ForeignKey(Vender, on_delete=models.CASCADE)
    is_payable = models.BooleanField(default=False)
    price = models.IntegerField(blank = True)
    pending = models.IntegerField(blank = True)
    paid = models.IntegerField(blank = True)
    image = models.ImageField(upload_to="service/")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
            while Service.objects.filter(id=self.id).exists():
                self.id = uuid.uuid4()
            self.slug = slugify(self.name, allow_unicode=True)
        super(Service, self).save()


class ForgetpasswordOtp(models.Model):
    id=models.UUIDField(editable=False,primary_key=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    otp = models.IntegerField()
    is_expire = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = uuid.uuid4()
            while ForgetpasswordOtp.objects.filter(id=self.id).exists():
                self.id = uuid.uuid4()
        super(ForgetpasswordOtp,self).save()



##### Signals ########
@receiver(post_save,sender=CustomUser)
def create_user_data(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            Admin.objects.create(cu=instance)#cu means CustomerUser Instace
        if instance.user_type==2:
            Vender.objects.create(cu=instance, pincode="", city=City.objects.first(), area=Area.objects.first(), address="", aletrnative_no = "", address_proof_type = "",address_proof_id="", address_proof_photo="",profile_photo="")
        if instance.user_type==3:
            Customer.objects.create(cu=instance, pincode="", city="", state="", address="")
    
    
@receiver(post_save,sender=CustomUser)
def save_user_data(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.admin.save()
    if instance.user_type==2:
        instance.vender.save()
    if instance.user_type==3:
        instance.customer.save()

@receiver(post_save,sender=PhoneOtp)
def set_expire_phone_otp(sender,instance,**kwargs):
    phone_otp = PhoneOtp.objects.filter(is_expire = False).exclude(id=instance.id)
    for p in phone_otp:
        otp_expire =  p.created_at + timedelta(minutes=5)
        if otp_expire > timezone.now():
            p.is_expire=True
            p.save()


@receiver(post_save,sender=EmailOtp)
def set_expire_email_otp(sender,instance,**kwargs):
    email_otp = EmailOtp.objects.filter(is_expire = False).exclude(id=instance.id)
    for e in email_otp:
        otp_expire =  e.created_at + timedelta(minutes=5)
        if otp_expire > timezone.now():
            e.is_expire=True
            e.save()

@receiver(post_save,sender=ForgetpasswordOtp)
def set_expire_forgetpassword_otp(sender,instance,**kwargs):
    forgetpassword_otp = ForgetpasswordOtp.objects.filter(is_expire = False).exclude(id=instance.id)
    for f in forgetpassword_otp:
        otp_expire =  f.created_at + timedelta(minutes=5)
        if otp_expire > timezone.now():
            f.is_expire=True
            f.save()