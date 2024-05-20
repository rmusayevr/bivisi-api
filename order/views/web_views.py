from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from ..models import Favorite, Basket, BasketItem
from ..serializers import (
    FavoriteWebReadSerializer,
    FavoriteCreateSerializer,
    BasketWebReadSerializer,
    BasketItemReadSerializer
)
from product.models import Product
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class FavoriteWebAPIView(ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteWebReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


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
    queryset = Basket.objects.all()
    serializer_class = BasketWebReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)


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
            'basket': BasketReadSerializer(basket).data
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
