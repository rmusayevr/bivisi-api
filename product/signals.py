from django.db.models.signals import post_save
from django.dispatch import receiver

from product.models import Product


@receiver(post_save, sender=Product)
def update_product_link(sender, instance, **kwargs):
    if not instance.product_link:
        instance.product_link = f"product_detail/{instance.pk}"
        instance.save(update_fields=['product_link'])
