from django.contrib import admin
from .models import Basket, BasketItem, Favorite
from import_export.admin import ImportExportModelAdmin


class FavoriteAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    search_fields = ('user__username', )
    list_filter = ('created_at', 'updated_at')


class BasketItemAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity',
                    'created_at', 'updated_at')
    search_fields = ('user__username', 'product')
    list_filter = ('created_at', 'updated_at')


class BasketAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'is_active', 'created_at', 'updated_at')
    search_fields = ('user__username', )
    list_filter = ('created_at', 'updated_at', 'is_active')


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(BasketItem, BasketItemAdmin)
admin.site.register(Basket, BasketAdmin)
