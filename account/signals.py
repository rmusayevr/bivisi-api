from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import OTPToken
from .utils.otp import generate_otp
from django.core.mail import send_mail
from django.utils import timezone


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            pass
        else:
            otp_code = generate_otp(instance.id)
            OTPToken.objects.create(user=instance, otp_code=otp_code, otp_expires_at=timezone.now(
            ) + timezone.timedelta(minutes=2))

            otp = OTPToken.objects.filter(user=instance).last()

            subject = "Email Verification"
            message = f"""
                                    Hi {instance.username}, here is your OTP {otp.otp_code}
                                    it expires in 2 minute, use the url below to redirect back to the website
                                    http://157.230.120.254/user/verify-otp

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
