from django.db import models
from product.models import Product
from account.models import User
from services.mixins import DateMixin


class Favorite(DateMixin):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_favorite")
    items = models.ManyToManyField(Product, related_name="favorite_products")

    def __str__(self):
        return f"{self.user.get_full_name()}'s favorite items"

    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"


class BasketItem(DateMixin):
    quantity = models.PositiveIntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                null=True, blank=True, related_name="product_basket_item")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_basket_item")

    def __str__(self):
        return f"{self.user.get_full_name()}'s basket item"

    def get_total(self):
        if self.product.in_sale:
            total = self.product.final_price*self.quantity
        else:
            total = self.product.price*self.quantity
        return total

    def get_subtotal(self):
        return self.product.price*self.quantity

    def get_sale(self):
        return self.get_subtotal() - self.get_total()

    class Meta:
        verbose_name = "Basket Item"
        verbose_name_plural = "Basket Items"


class Basket(DateMixin):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_basket")
    items = models.ManyToManyField(BasketItem, related_name="basket_items")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()}'s basket"

    class Meta:
        verbose_name = "Basket"
        verbose_name_plural = "Baskets"
