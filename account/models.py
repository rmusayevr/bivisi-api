from django.db import models
from django.conf import settings
from .managers import UserManager
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from services.mixins import DateMixin


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other")
    )
    STATUS_CHOICES = (
        ("Active", "Active"),
        ("De-active", "De-active"),
        ("Not Verified", "Not Verified")
    )

    username = models.CharField(_('username'), max_length=60, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)
    avatar = models.URLField(
        _("avatar"), max_length=500, null=True, blank=True)
    cover_image = models.URLField(
        _("cover image"), max_length=500, null=True, blank=True)
    gender = models.CharField(
        _('gender'), max_length=30, choices=GENDER_CHOICES, null=True, blank=True)
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    status = models.CharField(
        _('status'), max_length=20, choices=STATUS_CHOICES, default='Not Verified')
    is_active = models.BooleanField(_('active'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.username


class PhoneNumber(DateMixin):
    phone = PhoneNumberField(_('phone number'), unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_phone_number')

    class Meta:
        verbose_name = _('Phone Number')
        verbose_name_plural = _('Phone Numbers')

    def __str__(self):
        return f"{self.user.get_full_name()}'s phone number"


class OTPToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="user_otp_code")
    otp_code = models.CharField(max_length=6)
    tp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name()}'s OTP token"

    class Meta:
        verbose_name = _('OTP Token')
        verbose_name_plural = _('OTP Tokens')


class Subscription(DateMixin):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')
    follows = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
        unique_together = (('follower', 'follows'),)

    def __str__(self):
        return f"{self.follower.username} follows {self.follows.username}"
