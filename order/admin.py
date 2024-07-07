from django.contrib import admin
from .models import Basket, BasketItem, Favorite, Order
from import_export.admin import ImportExportModelAdmin


class FavoriteAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    search_fields = ('user__username', )
    list_filter = ('created_at', 'updated_at')


class BasketItemAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity',
                    'get_item_total', 'get_item_subtotal',
                    'created_at', 'updated_at', )
    search_fields = ('user__username', 'product')
    list_filter = ('created_at', 'updated_at')


class BasketAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'is_active', 'created_at', 'updated_at')
    search_fields = ('user__username', )
    list_filter = ('created_at', 'updated_at', 'is_active')


class OrderAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'basket', 'address')
    search_fields = ('user__username', )
    list_filter = ('created_at', 'updated_at')


admin.site.register(BasketItem, BasketItemAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Order, OrderAdmin)
