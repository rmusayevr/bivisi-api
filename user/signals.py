from django.conf import settings
from django.contrib.auth import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OTPToken, LoggedInUser
from .utils.otp import generate_otp
from django.core.mail import send_mail
from django.utils import timezone


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance, created, **kwargs):
    if created and instance.has_usable_password():
        if not instance.is_superuser and instance.sign_up_method == 'email':
            otp_code = generate_otp(instance.id)
            OTPToken.objects.create(user=instance, otp_code=otp_code, otp_expires_at=timezone.now(
            ) + timezone.timedelta(minutes=2))

            otp = OTPToken.objects.filter(user=instance).last()

            subject = "Email Verification"
            message = f"""
                                    Hi {instance.username}, here is your OTP {otp.otp_code}
                                    it expires in 2 minute, use the url below to redirect back to the website
                                    https://bivisifront.online/user/verify-otp

                                    """
            sender = settings.DEFAULT_FROM_EMAIL
            receiver = [instance.email, ]

            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )


@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user'))


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()
