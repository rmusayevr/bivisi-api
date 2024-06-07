from rest_framework import serializers
from order.models import BasketItem
from .models import Category, Product, ProductComment, ProductCommentLike, ProductVideoType, UserProductLike
from django.utils.translation import gettext_lazy as _


# ****************************************  <<<< CATEGORY START >>>>  ****************************************

class CategoryREADSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_name', 'created_at', 'updated_at']

    def get_parent_name(self, obj):
        visited_ids = self.context.get('visited_ids', set())

        # Check for cyclic relationships
        if obj.id in visited_ids or obj.parent_name is None:
            return None

        # Add the current object to the visited IDs
        visited_ids.add(obj.id)

        return CategoryREADSerializer(obj.parent_name, context={'visited_ids': visited_ids}).data


class CategoryCREATESerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_name', 'created_at', 'updated_at']

    def validate(self, data):
        parent = data.get('parent_name', None)
        if parent is not None and self.instance:
            if parent == self.instance:
                raise serializers.ValidationError(
                    _("A category cannot be its own parent."))
            if parent.is_descendant_of(self.instance):
                raise serializers.ValidationError(
                    _("Invalid parent assignment to prevent recursion."))
        return data


class CategoryWebSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'children']

    def get_children(self, obj):
        children = obj.parent_category_name.all()
        return CategoryWebSerializer(children, many=True).data

# ****************************************  <<<< CATEGORY END >>>>  ****************************************


# ****************************************  <<<< PRODUCT VIDEO TYPE START >>>>  ****************************************

class DashboardProductVideoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideoType
        fields = ['id', 'product_type', 'original_video', 'compressed_video',
                  'cover_image', 'product', 'created_at', 'updated_at']


class ProductForTypeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()  # Add this line

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'in_sale', 'percent', 'final_price', 'view_count',
                  'like_count', 'category', 'user', 'comment_count', 'created_at', 'updated_at']

    def get_user(self, obj):
        return {'id': obj.user.id, 'name': obj.user.username, 'avatar': obj.user.avatar.url if obj.user.avatar else None}

    def get_comment_count(self, obj):
        # Return the count of comments related to the product
        return obj.product_comment.count()


class WebProductVideoTypeSerializer(serializers.ModelSerializer):
    product = ProductForTypeSerializer(read_only=True)
    in_wishlist = serializers.SerializerMethodField()
    in_basket = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = ProductVideoType
        fields = ['id', 'product_type', 'original_video', 'compressed_video', 'cover_image',
                  'product', 'created_at', 'updated_at', 'in_wishlist', 'in_basket', 'is_liked']

    def get_in_wishlist(self, obj):
        request = self.context.get('request', None)
        if request is None or not request.user.is_authenticated:
            return False
        return obj.product.favorite_products.filter(user=request.user).exists()

    def get_in_basket(self, obj):
        request = self.context.get('request', None)
        if request is None or not request.user.is_authenticated:
            return False
        return BasketItem.objects.filter(user=request.user, product=obj.product).exists()

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request is None or not request.user.is_authenticated:
            return False
        return obj.product.user_product_like.filter(user=request.user).exists()

# ****************************************  <<<< PRODUCT VIDEO TYPE END >>>>   ****************************************


# ****************************************  <<<< PRODUCT START >>>>  ****************************************

class WebUploadProductCREATESerializer(serializers.ModelSerializer):

    product_type = serializers.ChoiceField(
        choices=ProductVideoType.product_types, write_only=True)
    cover_image = serializers.ImageField(
        required=False, allow_null=True, write_only=True)
    original_video = serializers.FileField(write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'in_sale', 'percent',
                  'category', 'product_type', 'cover_image', 'original_video']
        read_only_fields = ['user']

    def validate_percent(self, value):
        if value is not None and not (0 <= value <= 100):
            raise serializers.ValidationError(
                "Percent value must be between 0 and 100.")
        return value

    def create(self, validated_data):
        product_type = validated_data.pop('product_type')
        cover_image = validated_data.pop('cover_image', None)
        original_video = validated_data.pop('original_video')

        request = self.context.get('request')
        user = request.user
        validated_data['user'] = user

        product = super().create(validated_data)

        ProductVideoType.objects.create(
            product=product,
            product_type=product_type,
            cover_image=cover_image,
            original_video=original_video,
        )

        return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Assuming one-to-one relationship for simplicity
        product_video_type = instance.product_video_type.first()
        if product_video_type:
            representation['product_type'] = product_video_type.product_type
            representation['cover_image'] = product_video_type.cover_image.url if product_video_type.cover_image else None
            representation['original_video'] = product_video_type.original_video.url
        return representation


# class WebUploadProductUPDATESerializer(serializers.ModelSerializer):

#     product_type = serializers.ChoiceField(
#         choices=ProductVideoType.product_types, write_only=True, required=False)
#     cover_image = serializers.ImageField(
#         required=False, allow_null=True, write_only=True)
#     original_video = serializers.FileField(write_only=True, required=False)

#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'description', 'price', 'in_sale', 'percent',
#                   'category', 'product_type', 'cover_image', 'original_video']
#         read_only_fields = ['user']

#     def validate_percent(self, value):
#         if value is not None and not (0 <= value <= 100):
#             raise serializers.ValidationError(
#                 "Percent value must be between 0 and 100.")
#         return value

#     def update(self, instance, validated_data):
#         product_type = validated_data.pop('product_type', None)
#         cover_image = validated_data.pop('cover_image', None)
#         original_video = validated_data.pop('original_video', None)

#         request = self.context.get('request')
#         user = request.user
#         instance.user = user

#         instance = super().update(instance, validated_data)

#         product_video_type, created = ProductVideoType.objects.get_or_create(
#             pk=instance.pk).first()

#         if product_type:
#             product_video_type.product_type = product_type
#         if cover_image is not None:
#             product_video_type.cover_image = cover_image
#         if original_video is not None:
#             product_video_type.original_video = original_video
#         product_video_type.save()

#         return instance

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         # Assuming one-to-one relationship for simplicity
#         product_video_type = instance.product_video_type.first()
#         if product_video_type:
#             representation['product_type'] = product_video_type.product_type
#             representation['cover_image'] = product_video_type.cover_image.url if product_video_type.cover_image else None
#             representation['original_video'] = product_video_type.original_video.url
#         return representation


class ProductCREATESerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'in_sale', 'percent', 'final_price',
                  'view_count', 'like_count', 'category', 'user', 'created_at', 'updated_at']

    def validate_percent(self, value):
        if value is not None and not (0 <= value <= 100):
            raise serializers.ValidationError(
                "Percent value must be between 0 and 100.")
        return value


class ProductREADSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    product_video_type = DashboardProductVideoTypeSerializer(
        many=True, read_only=True)
    in_wishlist = serializers.SerializerMethodField()
    in_basket = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'product_video_type', 'price', 'in_sale', 'percent',
                  'final_price', 'view_count', 'like_count', 'category', 'user',
                  'in_wishlist', 'in_basket', 'is_liked', 'created_at', 'updated_at']

    def get_user(self, obj):
        return {'id': obj.user.id, 'name': obj.user.username, 'avatar': obj.user.avatar.url if obj.user.avatar else None}

    def get_in_wishlist(self, obj):
        request = self.context.get('request', None)
        if request is None or not request.user.is_authenticated:
            return False
        return obj.favorite_products.filter(user=request.user).exists()

    def get_in_basket(self, obj):
        request = self.context.get('request', None)
        if request is None or not request.user.is_authenticated:
            return False
        return BasketItem.objects.filter(user=request.user, product=obj).exists()

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request is None or not request.user.is_authenticated:
            return False
        return obj.user_product_like.filter(user=request.user).exists()

# ****************************************  <<<< PRODUCT END >>>>  ****************************************


# ****************************************  <<<< PRODUCT START >>>>  ****************************************

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

# ****************************************  <<<< PRODUCT END >>>>  ****************************************


# ****************************************  <<<< PRODUCT COMMENT START >>>>  ****************************************

class ProductCommentREADSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    parent_comment = serializers.SerializerMethodField()

    class Meta:
        model = ProductComment
        fields = ['id', 'comment', 'like_count', 'user', 'product',
                  'parent_comment', 'created_at', 'updated_at']

    def get_parent_comment(self, obj):
        if obj.parent_comment:
            return {
                'id': obj.parent_comment.id,
                'comment': obj.parent_comment.comment
            }
        return None

    def get_product(self, obj):
        return {'id': obj.product.id, 'name': obj.product.name}

    def get_user(self, obj):
        return {'id': obj.user.id, 'name': obj.user.username, 'avatar': obj.user.avatar.url if obj.user.avatar else None}


class ProductCommentCREATESerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductComment
        fields = ['id', 'comment', 'like_count', 'user', 'product',
                  'parent_comment', 'created_at', 'updated_at']

    def validate(self, data):
        parent = data.get('parent_comment', None)
        if parent is not None and self.instance:
            if parent == self.instance:
                raise serializers.ValidationError(
                    _("A comment cannot be its own parent."))
            if parent.is_descendant_of(self.instance):
                raise serializers.ValidationError(
                    _("Invalid parent assignment to prevent recursion."))
        return data


class WebProductCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = ProductComment
        fields = ['id', 'comment', 'like_count', 'user', 'product',
                  'parent_comment', 'created_at', 'updated_at']

    def get_user(self, obj):
        return {'id': obj.user.id, 'name': obj.user.username, 'avatar': obj.user.avatar.url if obj.user.avatar else None}

# ****************************************  <<<< PRODUCT COMMENT END >>>>  ****************************************


# ****************************************  <<<< PRODUCT COMMENT LIKE START >>>>  ****************************************

class ProductCommentLikeREADSerializer(serializers.ModelSerializer):
    product_comment = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()

    class Meta:
        model = ProductCommentLike
        fields = ['id', 'user', 'product_comment', 'created_at', 'updated_at']

    def get_product_comment(self, obj):
        return [{'id': product_comment.id, 'name': product_comment.comment} for product_comment in obj.product_comment.all()]


class ProductCommentLikeCREATESerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCommentLike
        fields = ['id', 'user', 'product_comment', 'created_at', 'updated_at']

# ****************************************  <<<< PRODUCT COMMENT LIKE END >>>>  ****************************************
