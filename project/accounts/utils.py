from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import random


def generate_otp():
    return f"{random.randint(100000, 999999)}"


def send_otp_email(user):
    otp_code = generate_otp()
    user.otp = otp_code
    user.expired_at = timezone.now() + timezone.timedelta(minutes=10)
    user.save()

    subject = "Your Email Verification OTP"
    message = f"""
    Dear {user.username},

    Thank you for registering with Drop Me.
    Your One-Time Password (OTP) for email verification is: {otp_code}

    For Security Don't share this code with anyone.
    If you did not request this OTP, please ignore this email.
    This code is valid for the next 10 minutes. Please enter this code to complete your verification process.

    Best regards,
    The Drop Me Team
    """

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


