from django.contrib import admin
from .models import Category, Product, UserProductLike, ProductComment, ProductCommentLike


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent_name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_type', 'price', 'final_price', 'in_sale', 'percent', 'view_count', 'like_count', 'user', 'video_url', 'created_at', 'updated_at')
    search_fields = ('name', )
    list_filter = ('product_type', 'in_sale', 'category', 'user', 'created_at', 'updated_at')
    filter_horizontal = ('category',)


class UserProductLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('user', 'product', 'created_at', 'updated_at')
    filter_horizontal = ('product',)


class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'product', 'like_count', 'parent_comment', 'created_at', 'updated_at')
    search_fields = ('comment', 'user__username', 'product__name')
    list_filter = ('user', 'product', 'created_at', 'updated_at')


class ProductCommentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'product_comment__comment')
    list_filter = ('user', 'product_comment', 'created_at', 'updated_at')
    filter_horizontal = ('product_comment',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(UserProductLike, UserProductLikeAdmin)
admin.site.register(ProductComment, ProductCommentAdmin)
admin.site.register(ProductCommentLike, ProductCommentLikeAdmin)
