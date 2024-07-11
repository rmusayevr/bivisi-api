from django.db import models
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _
from product.models import Product
from services.mixins import DateMixin
from services.uploader import Uploader


class Slider(DateMixin):
    image = models.ImageField(
        _("Image"), upload_to=Uploader.slider_image, max_length=500)

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Slider.objects.get(pk=self.pk)

            # Check if the image has been changed
            if self.image != old_instance.image:
                if old_instance.image:
                    old_instance.image.delete(save=False)

            # Check if the image has been cleared
            if not self.image:
                if old_instance.image:
                    old_instance.image.delete(save=False)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = _('Slider')
        verbose_name_plural = _('Sliders')


class FAQ(DateMixin):
    faq = models.CharField(_('faq'), max_length=300, unique=True)
    answer = models.CharField(_('answer'), max_length=300)
    is_active = models.BooleanField(_('is_active'), default=True)

    def __str__(self):
        return self.faq

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQ')


class Stream(DateMixin):
    room_id = models.CharField(_('room id'), max_length=100, unique=True)
    room_name = models.CharField(_('room name'), max_length=255)
    user_name = models.CharField(_('user name'), max_length=255)
    cover_image = models.ImageField(
        _('cover image'), upload_to=Uploader.stream_image, max_length=500)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_(
        'product'), related_name="stream_products", null=True, blank=True)

    def __str__(self):
        return f"{self.room_id} - {self.room_name} - {self.user_name} - {self.product}"

    class Meta:
        verbose_name = _('Stream')
        verbose_name_plural = _('Streams')
