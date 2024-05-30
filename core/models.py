import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from services.mixins import DateMixin
from services.uploader import Uploader


class Slider(DateMixin):
    image = models.ImageField(_("Image"), upload_to=Uploader.slider_image, max_length=500)

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
