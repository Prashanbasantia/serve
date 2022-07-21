from asyncio import constants
from cgi import print_directory
from django.conf import settings
from django.core.mail import send_mail,send_mass_mail,EmailMessage
from django.http import HttpResponseRedirect
from django.urls import reverse
def semd_register_otp_email(email,otp):
    email_from=settings.EMAIL_FROM_BILLING
    email_to = [email,]
    subject="Verify Email OTP NHI"
    message = str(otp)+" is your NHI Register OTP to verify your email. OTP is confidential. For security reasons, Do NOT share this OTP with anyone."
    msg = EmailMessage(
        subject,
        message,
        email_from,
        email_to,
        reply_to =[settings.EMAIL_REPLY_TO,],
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()

def OnlyAdminAccess(function):
    def _function(request,*args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        if request.user.user_type != '1':
            if request.user.user_type == '2':
                return HttpResponseRedirect('/vender/dashboard')
            else:
                return HttpResponseRedirect(reverse('account'))
        return function(request, *args, **kwargs)
    return _function

def OnlyVenderAccess(function):
    def _function(request,*args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        if request.user.user_type != '2':
            if request.user.user_type == '1':
                return HttpResponseRedirect('/admin/dashboard')
            else:
                return HttpResponseRedirect(reverse('account'))
        return function(request, *args, **kwargs)
    return _function


def OnlyUserAccess(function):
    def _function(request,*args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        if request.user.user_type != '3':
            if request.user.user_type == '2':
                return HttpResponseRedirect('/vender/dashboard')
            else:
                return HttpResponseRedirect('/admin/dashboard')
        return function(request, *args, **kwargs)
    return _function