from rest_framework import serializers
from .models import Category, Product, ProductComment, ProductCommentLike, UserProductLike


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_name', 'created_at', 'updated_at']


class ProductCREATESerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_type', 'name', 'description', 'video_url', 'price', 'in_sale', 'percent', 'final_price', 'view_count', 'like_count', 'category', 'user', 'created_at', 'updated_at']


class ProductREADSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['id', 'product_type', 'name', 'description', 'video_url', 'price', 'in_sale', 'percent', 'final_price', 'view_count', 'like_count', 'category', 'user', 'created_at', 'updated_at']


class UserProductLikeREADSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()

    class Meta:
        model = UserProductLike
        fields = ['id', 'user', 'product', 'created_at', 'updated_at']

    def get_product(self, obj):
        # If the relationship is Many-to-Many, we loop through and fetch required fields
        return [{'id': product.id, 'name': product.name} for product in obj.product.all()]


class UserProductLikeCREATESerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProductLike
        fields = ['id', 'user', 'product', 'created_at', 'updated_at']


class ProductCommentREADSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    product = serializers.SerializerMethodField()

    class Meta:
        model = ProductComment
        fields = ['id', 'comment', 'like_count', 'user', 'product', 'parent_comment', 'created_at', 'updated_at']

    def get_product(self, obj):
        # If the relationship is Many-to-Many, we loop through and fetch required fields
        return {'id': obj.product.id, 'name': obj.product.name}


class ProductCommentCREATESerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductComment
        fields = ['id', 'comment', 'like_count', 'user', 'product', 'parent_comment', 'created_at', 'updated_at']


class ProductCommentLikeREADSerializer(serializers.ModelSerializer):
    product_comment = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()

    class Meta:
        model = ProductCommentLike
        fields = ['id', 'user', 'product_comment', 'created_at', 'updated_at']

    def get_product(self, obj):
        # If the relationship is Many-to-Many, we loop through and fetch required fields
        return [{'id': product_comment.id, 'name': product_comment.name} for product_comment in obj.product_comment.all()]


class ProductCommentLikeCREATESerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCommentLike
        fields = ['id', 'user', 'product_comment', 'created_at', 'updated_at']

