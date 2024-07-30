from django.contrib import admin
from .models import Category, Product, ProductComment, ProductCommentLike, ProductPropertyAndValue, ProductVideoType, UserProductLike
from import_export.admin import ImportExportModelAdmin


class CategoryAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "name",
        "parent_name",
        "created_at",
        "updated_at"
    ]
    list_display_links = ["name"]
    search_fields = ["name"]
    list_filter = ["parent_name", "created_at", "updated_at"]
    list_per_page = 15
    autocomplete_fields = ["parent_name"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("parent_name")


class ProductAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "name",
        "price",
        "final_price",
        "user",
        "created_at",
        "updated_at"
    ]
    list_display_links = ["name"]
    search_fields = ["name"]
    list_filter = [
        "in_sale",
        "category",
        "user",
        "created_at",
        "updated_at"
    ]
    list_per_page = 15
    autocomplete_fields = ["category", "user"]
    filter_horizontal = ["category"]

    fieldsets = [
        ("General Information", {
            "fields": [
                "name",
                "description",
                "price",
                "in_sale",
                "percent",
                "final_price",
                "is_premium",
            ],
        }),
        ("Additional Information", {
            "fields": [
                "user",
                "phone_number",
                "product_link",
                "view_count",
                "like_count",
                "location",
                "location_url",
            ],
        }),
        ("Categories", {
            "fields": ["category"],
            "classes": ["tab_category", "deferred"],
        }),
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user").prefetch_related("category")


class ProductVideoTypeAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "product_type",
        "product",
        "created_at",
        "updated_at"
    ]
    list_display_links = ["product_type", "product"]
    search_fields = ["product__name"]
    list_filter = [
        "product",
        "product_type",
        "created_at",
        "updated_at"
    ]
    fieldsets = [
        ("Product Information", {
            "fields": [
                "product",
                "product_type",
            ],
        }),
        ("Media Information", {
            "fields": [
                "cover_image",
                "original_video",
                "compressed_video",
            ],
        }),
    ]
    autocomplete_fields = ["product"]
    list_per_page = 15

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("product")

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.cover_image:
                obj.cover_image.delete(save=False)

            if obj.original_video:
                obj.original_video.delete(save=False)

        super().delete_queryset(request, queryset)


class UserProductLikeAdmin(ImportExportModelAdmin):
    list_display = ["id", "user", "created_at", "updated_at"]
    list_display_links = ["user"]
    search_fields = ["user__username", "product__name"]
    list_filter = ["user", "product", "created_at", "updated_at"]
    filter_horizontal = ["product"]
    autocomplete_fields = ["product"]
    list_per_page = 15

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user").prefetch_related("product")


class ProductCommentAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "comment",
        "user",
        "product",
        "like_count",
        "parent_comment",
        "created_at",
        "updated_at"
    ]
    list_display_links = ["user"]
    search_fields = ["comment", "user__username", "product__name"]
    list_filter = [
        "user",
        "product",
        "parent_comment",
        "created_at",
        "updated_at"
    ]
    list_per_page = 15

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user", "product", "parent_comment")


class ProductCommentLikeAdmin(ImportExportModelAdmin):
    list_display = ["id",  "user", "created_at", "updated_at"]
    list_display_links = ["user"]
    search_fields = ["user__username", "product_comment__comment"]
    list_filter = ["user", "product_comment", "created_at", "updated_at"]
    filter_horizontal = ["product_comment"]
    autocomplete_fields = ["product_comment"]
    list_per_page = 15

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user").prefetch_related("product_comment")


class ProductPropertyAndValueAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "product_property",
        "property_value",
        "product",
        "created_at",
        "updated_at"
    ]
    list_display_links = ["product_property", "property_value"]
    search_fields = ["product_property", "property_value", "product__name"]
    list_filter = ["product", "created_at", "updated_at"]
    autocomplete_fields = ["product"]
    list_per_page = 15

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("product")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVideoType, ProductVideoTypeAdmin)
admin.site.register(UserProductLike, UserProductLikeAdmin)
admin.site.register(ProductComment, ProductCommentAdmin)
admin.site.register(ProductCommentLike, ProductCommentLikeAdmin)
admin.site.register(ProductPropertyAndValue, ProductPropertyAndValueAdmin)
