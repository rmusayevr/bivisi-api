from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from services.mixins import DateMixin
from account.models import User
from django.core.exceptions import ValidationError


class Category(DateMixin):
    name = models.CharField(_("Name"), max_length=255)
    parent_name = models.ForeignKey("Category", verbose_name=_(
        "Parent Name"), on_delete=models.CASCADE, related_name='parent_category_name', null=True, blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self == self.parent_name:
            raise ValidationError(_("A category cannot be its own parent."))
        if self.parent_name and self.parent_name.is_descendant_of(self):
            raise ValidationError(
                _("Invalid parent assignment to prevent recursion."))

    def is_descendant_of(self, other):
        current = self
        while current.parent_name is not None:
            if current.parent_name == other:
                return True
            current = current.parent_name
        return False

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Product(DateMixin):

    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"))

    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    in_sale = models.BooleanField(_("In Sale"), default=False)
    percent = models.PositiveIntegerField(_("Percent"), null=True, blank=True)
    final_price = models.DecimalField(
        _("Final Price"), max_digits=10, decimal_places=2, null=True, blank=True)

    view_count = models.PositiveIntegerField(_("View Count"), default=0)
    like_count = models.PositiveIntegerField(_("Like Count"), default=0)

    category = models.ManyToManyField(Category, verbose_name=_(
        "Category"), related_name='product_categories')
    user = models.ForeignKey(User, verbose_name=_(
        "user"), on_delete=models.CASCADE, related_name='user_products')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.in_sale and self.percent is not None:
            # Ensure percent is within the valid range
            if not (0 <= self.percent <= 100):
                raise ValidationError(
                    _("Percent value must be between 0 and 100."))

            # Convert to Decimal to ensure correct calculation
            discount_multiplier = Decimal(
                1) - Decimal(self.percent) / Decimal(100)
            self.final_price = self.price * discount_multiplier

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class ProductVideoType(DateMixin):
    product_types = (
        ('Video', 'Video'),
        ('Shorts', 'Shorts')
    )
    product_type = models.CharField(
        _("Product Type"), max_length=255, choices=product_types)

    cover_image_url = models.URLField(
        _("Cover Image"), max_length=255, null=True, blank=True)

    video_url = models.URLField(_("Video Url"), max_length=255)
    product = models.ForeignKey(Product, verbose_name=_(
        "Product"), on_delete=models.CASCADE, related_name='product_video_type')

    def __str__(self):
        return f"{self.product.name} - {self.product_type}"

    class Meta:
        verbose_name = _('Product Video & Type')
        verbose_name_plural = _('Product Videos & Types')


class UserProductLike(DateMixin):
    user = models.OneToOneField(User, verbose_name=_(
        "User"), on_delete=models.CASCADE, related_name='user_like')
    product = models.ManyToManyField(Product, verbose_name=_(
        "Product"), related_name='user_product_like')

    def __str__(self):
        return f"{self.user.username} - products like"

    class Meta:
        verbose_name = _('Product Like')
        verbose_name_plural = _('Products Like')


class ProductComment(DateMixin):
    comment = models.TextField(_("Comment"))

    like_count = models.IntegerField(_("Like Count"), default=0)

    user = models.ForeignKey(User, verbose_name=_(
        "User"), on_delete=models.CASCADE, related_name='user_comment')
    product = models.ForeignKey(Product, verbose_name=_(
        "Product"), on_delete=models.CASCADE, related_name='product_comment')
    parent_comment = models.ForeignKey("ProductComment", verbose_name=_(
        "Parent Comment"), on_delete=models.CASCADE, related_name='comment_child', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} comment"

    def clean(self):
        if self == self.parent_comment:
            raise ValidationError(_("A comment cannot be its own parent."))
        if self.parent_comment and self.parent_comment.is_descendant_of(self):
            raise ValidationError(
                _("Invalid parent assignment to prevent recursion."))

    def is_descendant_of(self, other):
        current = self
        while current.parent_comment is not None:
            if current.parent_comment == other:
                return True
            current = current.parent_comment
        return False

    class Meta:
        verbose_name = _('Product Comment')
        verbose_name_plural = _('Product Comments')


class ProductCommentLike(DateMixin):
    user = models.OneToOneField(User, verbose_name=_(
        "User"), on_delete=models.CASCADE, related_name='user_comment_like')
    product_comment = models.ManyToManyField(ProductComment, verbose_name=_(
        "Product Comment"), related_name='user_product_comment_like')

    def __str__(self):
        return f"{self.user.username} - product comments like"

    class Meta:
        verbose_name = _('Product Comment Like')
        verbose_name_plural = _('Product Comments Like')


class UserProductHistory(DateMixin):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_history')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_history')
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s history"

    class Meta:
        verbose_name = _('History')
        verbose_name_plural = _('Histories')
