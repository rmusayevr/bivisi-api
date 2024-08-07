from django.db import models
from django.conf import settings
from services.uploader import Uploader
from .managers import UserManager
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from services.mixins import DateMixin
from django_countries.fields import CountryField


class ChannelCategory(DateMixin):
    name = models.CharField(_('channel category name'),
                            max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Channel Category')
        verbose_name_plural = _('Channel Categories')


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
    sign_up_method = models.CharField(
        _('sign up method'), max_length=30, default='email')

    username = models.CharField(_('username'), max_length=60, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=60)
    avatar = models.ImageField(
        _("avatar"), upload_to=Uploader.user_avatar, max_length=500, null=True, blank=True)
    cover_image = models.ImageField(
        _("cover image"), upload_to=Uploader.user_cover_image, max_length=500, null=True, blank=True)
    gender = models.CharField(
        _('gender'), max_length=30, choices=GENDER_CHOICES, null=True, blank=True)
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    status = models.CharField(
        _('status'), max_length=20, choices=STATUS_CHOICES, default='Not Verified')
    is_active = models.BooleanField(_('active'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    token = models.CharField(
        max_length=1024, blank=True, null=True
    )

    bio = models.TextField(_("About"), null=True, blank=True)

    instagram = models.URLField(
        _("Instagram"), max_length=255, null=True, blank=True)
    twitter = models.URLField(
        _("Twitter"), max_length=255, null=True, blank=True)
    facebook = models.URLField(
        _("Facebook"), max_length=255, null=True, blank=True)

    categories = models.ManyToManyField(
        ChannelCategory, related_name='channel_categories', blank=True)

    country = CountryField(null=True)

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

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = User.objects.get(pk=self.pk)

            # Check if the avatar has been changed
            if self.avatar != old_instance.avatar:
                if old_instance.avatar:
                    old_instance.avatar.delete(save=False)

            # Check if the avatar has been cleared
            if not self.avatar:
                if old_instance.avatar:
                    old_instance.avatar.delete(save=False)

            # Check if the cover image has been changed
            if self.cover_image != old_instance.cover_image:
                if old_instance.cover_image:
                    old_instance.cover_image.delete(save=False)

            # Check if the cover image has been cleared
            if not self.cover_image:
                if old_instance.cover_image:
                    old_instance.cover_image.delete(save=False)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.avatar:
            self.avatar.delete(save=False)

        if self.cover_image:
            self.cover_image.delete(save=False)
        super().delete(*args, **kwargs)


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


class Chats(DateMixin):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user_chats")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user_chats")
    last_message = models.TextField()

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')

    def __str__(self):
        return f"Chat between {self.from_user.username} and {self.to_user.username}"


class Messages(DateMixin):
    chat = models.ForeignKey(Chats, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    media = models.FileField(
        upload_to=Uploader.user_chat_media, null=True, blank=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __str__(self):
        return f"{self.user.username}'s chat messages with {self.chat.to_user}"
