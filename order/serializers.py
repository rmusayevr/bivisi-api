from rest_framework import serializers
from order.models import Favorite, Basket, BasketItem
from product.models import ProductVideoType
from product.serializers import ProductREADSerializer, WebProductVideoTypeSerializer


class FavoriteReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'items']

    def get_items(self, obj):
        return [{'id': product.id, 'name': product.name} for product in obj.items.all()]


class FavoriteWebReadSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ['items']

    def get_items(self, obj):
        request = self.context.get('request')
        product_type = request.query_params.get('product_type')
        product_video_types = ProductVideoType.objects.filter(product__in=obj.items.all())

        if product_type:
            product_video_types = product_video_types.filter(product_type=product_type)

        return WebProductVideoTypeSerializer(product_video_types, many=True).data


class FavoriteCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'items']


class BasketItemReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    product = serializers.SerializerMethodField()

    class Meta:
        model = BasketItem
        fields = ['id', 'user', 'product', 'quantity']

    def get_product(self, obj):
        return {'id': obj.product.id, 'name': obj.product.name}


class BasketItemWebReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    product = ProductREADSerializer()

    class Meta:
        model = BasketItem
        fields = ['id', 'user', 'product', 'quantity']


class BasketItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasketItem
        fields = ['id', 'user', 'product', 'quantity']


class BasketReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ['id', 'user', 'items', 'is_active']

    def get_items(self, obj):
        return [{'id': product.product.id, 'name': product.product.name, 'quantity': product.quantity} for product in obj.items.all()]


class BasketWebReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    items = BasketItemWebReadSerializer(many=True)

    class Meta:
        model = Basket
        fields = ['id', 'user', 'items', 'is_active']


class BasketCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basket
        fields = ['id', 'user', 'items', 'is_active']
