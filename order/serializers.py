from rest_framework import serializers
from order.models import Wishlist, Basket, BasketItem
from product.serializers import ProductREADSerializer


class WishlistSerializer(serializers.ModelSerializer):
    items = ProductREADSerializer()

    class Meta:
        model = Wishlist
        fields = [
            'user',
            'items'
        ]


class BasketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basket
        fields = [
            'user',
            'items'
        ]


class BasketItemSerializer(serializers.ModelSerializer):
    product = ProductREADSerializer()

    class Meta:
        model = BasketItem
        fields = [
            'user',
            'product',
            'quantity'
        ]
