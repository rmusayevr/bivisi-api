from rest_framework import serializers
from product.models import Product, ProductVideoType
from .models import UserHistory



class ProductFORHISTORYSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'in_sale', 'percent', 'final_price']


class ProductVideoTypeFORHISTORYSerializer(serializers.ModelSerializer):
    product = ProductFORHISTORYSerializer()

    class Meta:
        model = ProductVideoType
        fields = ['id', 'product_type', 'cover_image_url', 'video_url', 'product']


class UserHistorySerializer(serializers.ModelSerializer):
    product_video_type = ProductVideoTypeFORHISTORYSerializer()

    class Meta:
        model = UserHistory
        fields = ['id', 'user', 'watch_date', 'product_video_type']


class UserHistoryDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate_id(self, value):
        user = self.context['request'].user
        if not UserHistory.objects.filter(pk=value, user=user).exists():
            raise serializers.ValidationError("Invalid UserHistory ID or unauthorized access.")
        return value
