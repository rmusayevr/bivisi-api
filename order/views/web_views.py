from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from product.serializers import WebProductVideoTypeSerializer
from ..models import Basket, BasketItem, Favorite, Order
from ..serializers import (
    BasketItemReadSerializer,
    BasketWebReadSerializer,
    FavoriteCreateSerializer,
    OrderCreateSerializer,
    OrderListSerializer,
)
from product.models import Product, ProductVideoType
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from services.pagination import InfiniteScrollPagination


class FavoriteWebAPIView(ListAPIView):
    serializer_class = WebProductVideoTypeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = InfiniteScrollPagination

    def get_queryset(self):
        user = self.request.user
        product_type = self.request.GET.get('product_type')
        favorite_product_ids = Favorite.objects.filter(
            user=user).values_list('items__id', flat=True)
        queryset = ProductVideoType.objects.filter(
            product_id__in=favorite_product_ids)

        if product_type:
            queryset = queryset.filter(product_type=product_type)

        return queryset


class ToggleFavoriteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        product = get_object_or_404(Product, pk=pk)

        if product.user == user:
            return Response({'error': 'You cannot favorite your own product.'}, status=status.HTTP_400_BAD_REQUEST)

        favorite, created = Favorite.objects.get_or_create(user=user)

        if product in favorite.items.all():
            favorite.items.remove(product)
            message = "Product removed from favorites."
        else:
            favorite.items.add(product)
            message = "Product added to favorites."

        favorite.save()

        return Response({
            'message': message,
            'favorite': FavoriteCreateSerializer(favorite).data
        }, status=status.HTTP_200_OK)


class BasketWebAPIView(ListAPIView):
    serializer_class = BasketWebReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user, is_active=True).select_related("user")


class AddBasketAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        product = get_object_or_404(Product, pk=pk)
        quantity = request.data.get('quantity', 1)

        if product.user == user:
            return Response({'error': 'You cannot add your own product to the basket.'}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(quantity, int) or quantity < 1:
            return Response({'error': 'Invalid quantity provided.'}, status=status.HTTP_400_BAD_REQUEST)

        basket, created = Basket.objects.get_or_create(
            user=user, is_active=True)

        try:
            basket_item = BasketItem.objects.get(user=user, product=product)
            basket_item.quantity += quantity
            basket_item.save()
            message = "Product quantity increased in basket."
        except BasketItem.DoesNotExist:
            basket_item = BasketItem.objects.create(
                user=user, product=product, quantity=1)
            basket.items.add(basket_item)
            message = "Product added to basket."

        basket.save()

        return Response({
            'message': message,
            'basket': BasketWebReadSerializer(basket).data
        }, status=status.HTTP_200_OK)


class ChangeBasketItemAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']

    def put(self, request, pk, *args, **kwargs):
        user = request.user
        product = get_object_or_404(Product, pk=pk)
        quantity = request.data.get('quantity')

        if not isinstance(quantity, int) or quantity < 1:
            return Response({'error': 'Invalid quantity provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            basket_item = BasketItem.objects.get(user=user, product=product)
            basket_item.quantity = quantity
            basket_item.save()
        except BasketItem.DoesNotExist:
            return Response({'message': 'Product not found in basket.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'message': "Product quantity changed in basket.",
            'basket': BasketItemReadSerializer(basket_item).data
        }, status=status.HTTP_200_OK)


class DeleteBasketItemAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['delete']

    def delete(self, request, pk, *args, **kwargs):
        user = request.user
        product = get_object_or_404(Product, pk=pk)
        try:
            basket_item = BasketItem.objects.get(user=user, product=product)
            basket_item.delete()
            message = "Product removed from basket."
        except BasketItem.DoesNotExist:
            return Response({'message': 'Product not found in basket.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': message}, status=status.HTTP_200_OK)


class DeleteBasketAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['delete']

    def delete(self, request, *args, **kwargs):
        user = request.user
        try:
            basket = Basket.objects.get(user=user, is_active=True)
            basket.items.all().delete()
            basket.delete()
            message = "Basket deleted successfully."
            return Response({'message': message}, status=status.HTTP_200_OK)
        except Basket.DoesNotExist:
            return Response({'message': 'Basket not found.'}, status=status.HTTP_404_NOT_FOUND)


class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related("user")


class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
