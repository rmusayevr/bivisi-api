from rest_framework import serializers
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
                raise serializers.ValidationError(_("A category cannot be its own parent."))
            if parent.is_descendant_of(self.instance):
                raise serializers.ValidationError(_("Invalid parent assignment to prevent recursion."))
        return data

# ****************************************  <<<< CATEGORY END >>>>  ****************************************


# ****************************************  <<<< PRODUCT VIDEO TYPE START >>>>  ****************************************

class DashboardProductVideoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideoType
        fields = ['id', 'product_type', 'video_url', 'cover_image_url','product', 'created_at', 'updated_at']


class ProductForTypeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()  # Add this line

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'in_sale', 'percent', 'final_price', 'view_count', 'like_count', 'category', 'user', 'comment_count', 'created_at', 'updated_at']

    def get_user(self, obj):
        return {'id': obj.user.id, 'name': obj.user.username, 'avatar': obj.user.avatar if obj.user.avatar else None}

    def get_comment_count(self, obj):
        # Return the count of comments related to the product
        return obj.product_comment.count()


class WebProductVideoTypeSerializer(serializers.ModelSerializer):
    product = ProductForTypeSerializer(read_only=True)

    class Meta:
        model = ProductVideoType
        fields = ['id', 'product_type', 'video_url', 'cover_image_url','product', 'created_at', 'updated_at']

# ****************************************  <<<< PRODUCT VIDEO TYPE END >>>>   ****************************************


# ****************************************  <<<< PRODUCT START >>>>  ****************************************

class ProductCREATESerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'in_sale', 'percent', 'final_price', 'view_count', 'like_count', 'category', 'user', 'created_at', 'updated_at']

    def validate_percent(self, value):
        if value is not None and not (0 <= value <= 100):
            raise serializers.ValidationError("Percent value must be between 0 and 100.")
        return value


class ProductREADSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    product_video_type = DashboardProductVideoTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'product_video_type', 'price', 'in_sale', 'percent', 'final_price', 'view_count', 'like_count', 'category', 'user', 'created_at', 'updated_at']

    def get_user(self, obj):
        return {'id': obj.user.id, 'name': obj.user.username, 'avatar': obj.user.avatar if obj.user.avatar else None}

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
        fields = ['id', 'comment', 'like_count', 'user', 'product', 'parent_comment', 'created_at', 'updated_at']

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
        return {'id': obj.user.id, 'name': obj.user.username, 'avatar': obj.user.avatar if obj.user.avatar else None}


class ProductCommentCREATESerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductComment
        fields = ['id', 'comment', 'like_count', 'user', 'product', 'parent_comment', 'created_at', 'updated_at']

    def validate(self, data):
        parent = data.get('parent_comment', None)
        if parent is not None and self.instance:
            if parent == self.instance:
                raise serializers.ValidationError(_("A comment cannot be its own parent."))
            if parent.is_descendant_of(self.instance):
                raise serializers.ValidationError(_("Invalid parent assignment to prevent recursion."))
        return data


class WebProductCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = ProductComment
        fields = ['id', 'comment', 'like_count', 'user', 'product', 'parent_comment', 'created_at', 'updated_at']

    def get_user(self, obj):
        return {'id': obj.user.id, 'name': obj.user.username, 'avatar': obj.user.avatar if obj.user.avatar else None}

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
