from django.contrib import admin
from .models import Category, Product, ProductComment, ProductCommentLike, ProductVideoType, UserProductLike
from import_export.admin import ImportExportModelAdmin


class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'parent_name', 'created_at', 'updated_at')
    search_fields = ('name', )
    list_filter = ('created_at', 'updated_at')


class ProductAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'price', 'final_price', 'in_sale', 'percent',
                    'view_count', 'like_count', 'user', 'created_at', 'updated_at')
    search_fields = ('name', )
    list_filter = ('in_sale', 'category', 'user', 'created_at', 'updated_at')
    filter_horizontal = ('category', )


class ProductVideoTypeAdmin(ImportExportModelAdmin):
    list_display = ('id', 'product', 'product_type',
                    'video_url', 'created_at', 'updated_at')
    search_fields = ('product__name', )
    list_filter = ('product', 'product_type')


class UserProductLikeAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('user', 'product', 'created_at', 'updated_at')
    filter_horizontal = ('product', )


class ProductCommentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'comment', 'user', 'product',
                    'like_count', 'parent_comment', 'created_at', 'updated_at')
    search_fields = ('comment', 'user__username', 'product__name')
    list_filter = ('user', 'product', 'created_at', 'updated_at')


class ProductCommentLikeAdmin(ImportExportModelAdmin):
    list_display = ('id',  'user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'product_comment__comment')
    list_filter = ('user', 'product_comment', 'created_at', 'updated_at')
    filter_horizontal = ('product_comment', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVideoType, ProductVideoTypeAdmin)
admin.site.register(UserProductLike, UserProductLikeAdmin)
admin.site.register(ProductComment, ProductCommentAdmin)
admin.site.register(ProductCommentLike, ProductCommentLikeAdmin)
