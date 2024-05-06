from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from services.mixins import DateMixin
from services.uploader import Uploader
from account.models import User


class Category(DateMixin):
    name = models.CharField(_("Name"), max_length=255)
    parent_name = models.ForeignKey("Category", verbose_name=_("Parent Name"), on_delete=models.CASCADE, related_name='parent_category_name', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Product(DateMixin):
    product_types = (
        ('Video', 'Video'),
        ('Shorts', 'Shorts')
    )
    product_type = models.CharField(_("Product Type"), max_length=255, choices=product_types)

    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"))
    video_url = models.URLField(_("Video Url"), max_length=255)

    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    in_sale = models.BooleanField(_("In Sale"), default=False)
    percent = models.IntegerField(_("Percent"), null=True, blank=True)
    final_price = models.DecimalField(_("Final Price"), max_digits=10, decimal_places=2, null=True, blank=True)

    view_count = models.IntegerField(_("View Count"), default=0)
    like_count = models.IntegerField(_("Like Count"), default=0)

    category = models.ManyToManyField(Category, verbose_name=_("Category"), related_name='product_categories')
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE, related_name='user_products')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.in_sale and self.percent is not None:
            # Ensure percent is within the valid range
            if not (0 <= self.percent <= 100):
                raise ValueError("Percent value must be between 0 and 100.")

            # Convert to Decimal to ensure correct calculation
            discount_multiplier = Decimal(1) - Decimal(self.percent) / Decimal(100)
            self.final_price = self.price * discount_multiplier

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class UserProductLike(DateMixin):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name='user_like')
    product = models.ManyToManyField(Product, verbose_name=_("Product"), related_name='user_product_like')

    def __str__(self):
        return f"{self.user.username} - products like"

    class Meta:
        verbose_name = _('Product Like')
        verbose_name_plural = _('Products Like')


class ProductComment(DateMixin):
    comment = models.TextField(_("Comment"))

    like_count = models.IntegerField(_("Like Count"), default=0)

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name='user_comment')
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name='product_comment')
    parent_comment = models.ForeignKey("ProductComment", verbose_name=_("Parent Comment"), on_delete=models.CASCADE, related_name='parent_comments', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} comment"

    class Meta:
        verbose_name = _('Product Comment')
        verbose_name_plural = _('Product Comments')


class ProductCommentLike(DateMixin):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name='user_comment_like')
    product_comment = models.ManyToManyField(ProductComment, verbose_name=_("Product Comment"), related_name='user_product_comment_like')

    def __str__(self):
        return f"{self.user.username} - product comments like"

    class Meta:
        verbose_name = _('Product Comment Like')
        verbose_name_plural = _('Product Comments Like')
