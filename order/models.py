from django.db import models
from product.models import Product
from user.models import User
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
        indexes = [
            models.Index(fields=['user']),
        ]


class BasketItem(DateMixin):
    quantity = models.PositiveIntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                null=True, blank=True, related_name="product_basket_item")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_basket_item")

    def __str__(self):
        return f"{self.user.get_full_name()}'s basket item"

    def get_item_total(self):
        if self.product.in_sale:
            total = self.product.final_price*self.quantity
        else:
            total = self.product.price*self.quantity
        return total

    def get_item_subtotal(self):
        return self.product.price*self.quantity

    def get_item_sale(self):
        return self.get_item_subtotal() - self.get_item_total()

    class Meta:
        verbose_name = "Basket Item"
        verbose_name_plural = "Basket Items"
        indexes = [
            models.Index(fields=['user', 'product']),
        ]


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
        indexes = [
            models.Index(fields=['user', 'is_active']),
        ]

class Order(DateMixin):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_order',)
    basket = models.ForeignKey(
        Basket, on_delete=models.CASCADE, related_name='order_products')
    address = models.TextField()

    def __str__(self):
        return f"{self.user.get_full_name()}'s order"
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        indexes = [
            models.Index(fields=['user', 'basket']),
        ]
