from django.contrib import admin
from .models import Basket, BasketItem, Wishlist

admin.site.register(Basket)
admin.site.register(BasketItem)
admin.site.register(Wishlist)

