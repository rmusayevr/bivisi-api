import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from services.mixins import DateMixin
from services.uploader import Uploader


class Slider(DateMixin):
    image = models.ImageField(_("Image"), upload_to=Uploader.slider_image, max_length=500)

    def save(self, *args, **kwargs):

        if self.pk:
            # Retrieve the existing instance from the database
            old_instance = Slider.objects.get(pk=self.pk)

            # Check if the image has been changed
            if self.image != old_instance.image:
                # Delete old images if they exist
                if old_instance.image:
                    # Delete original image
                    if os.path.isfile(old_instance.image.path):
                        os.remove(old_instance.image.path)

            # Check if the image has been cleared
            if not self.image:
                # Delete old images if they exist
                if old_instance.image:
                    # Delete original image
                    if os.path.isfile(old_instance.image.path):
                        os.remove(old_instance.image.path)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the images associated with the blog instance
        if self.image:
            storage, path = self.image.storage, self.image.path
            storage.delete(path)

        # Call the delete method of the parent class
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = _('Slider')
        verbose_name_plural = _('Sliders')

