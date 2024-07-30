from django.contrib import admin
from .models import Basket, BasketItem, Favorite, Order
from import_export.admin import ImportExportModelAdmin


class FavoriteAdmin(ImportExportModelAdmin):
    list_display = ["id", "user", "created_at", "updated_at"]
    list_display_links = ["user"]
    search_fields = ["user__username"]
    list_filter = ["created_at", "updated_at"]
    autocomplete_fields = ["items"]
    list_per_page = 15

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user").prefetch_related("items")


class BasketItemAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "user",
        "product",
        "quantity",
        "created_at",
        "updated_at"
    ]
    list_display_links = ["user", "product"]
    search_fields = ["user__username", "product"]
    list_filter = ["created_at", "updated_at"]
    autocomplete_fields = ["product"]
    list_per_page = 15

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user", "product")


class BasketAdmin(ImportExportModelAdmin):
    list_display = ["id", "user", "is_active", "created_at", "updated_at"]
    list_display_links = ["user"]
    search_fields = ["user__username"]
    list_filter = ["created_at", "updated_at", "is_active"]
    autocomplete_fields = ["items"]
    list_per_page = 15

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user").prefetch_related("items")

class OrderAdmin(ImportExportModelAdmin):
    list_display = ["id", "user", "basket", "created_at", "updated_at"]
    list_display_links = ["user", "basket"]
    search_fields = ["user__username"]
    list_filter = ["created_at", "updated_at"]
    list_per_page = 15

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user", "basket")


admin.site.register(BasketItem, BasketItemAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Order, OrderAdmin)
