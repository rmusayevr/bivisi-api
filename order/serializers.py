from rest_framework import serializers
from order.models import Basket, BasketItem, Favorite, Order
from product.serializers import ProductREADSerializer


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
    total = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    sale = serializers.SerializerMethodField()

    class Meta:
        model = BasketItem
        fields = ['id', 'user', 'product',
                  'quantity', 'total', 'subtotal', 'sale']

    def get_product(self, obj):
        return {'id': obj.product.id, 'name': obj.product.name}

    def get_total(self, obj):
        return obj.get_item_total()

    def get_subtotal(self, obj):
        return obj.get_item_subtotal()

    def get_sale(self, obj):
        return obj.get_item_sale()


class BasketItemWebReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    product = ProductREADSerializer()
    total = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    sale = serializers.SerializerMethodField()

    class Meta:
        model = BasketItem
        fields = ['id', 'user', 'product',
                  'quantity', 'total', 'subtotal', 'sale']

    def get_total(self, obj):
        return obj.get_item_total()

    def get_subtotal(self, obj):
        return obj.get_item_subtotal()

    def get_sale(self, obj):
        return obj.get_item_sale()


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


class OrderReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'basket', 'address']


class OrderListSerializer(serializers.ModelSerializer):
    basket = BasketWebReadSerializer()
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'basket', 'address']


class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'user', 'basket', 'address']
