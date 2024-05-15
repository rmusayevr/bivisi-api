from rest_framework import serializers
from order.models import Favorite, Basket, BasketItem


class FavoriteReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'items']

    def get_items(self, obj):
        return [{'id': product.id, 'name': product.name} for product in obj.items.all()]


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


class BasketCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basket
        fields = ['id', 'user', 'items', 'is_active']
