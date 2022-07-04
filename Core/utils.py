from django.conf import settings
from django.core.mail import send_mail,send_mass_mail,EmailMessage

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