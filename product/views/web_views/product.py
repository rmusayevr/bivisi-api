import django_filters.rest_framework
from rest_framework import filters, status
from django.db.models import Count
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from product.filters import ProductFilter
from product.models import (
    Product,
    ProductVideoType,
    UserProductLike
)
from product.serializers import (
    ProductPremiumUpdateSerializer,
    WebProductVideoTypeSerializer,
    WebUploadProductCREATESerializer,
    WebUploadProductUPDATESerializer,
    ProductREADSerializer,
)
from services.pagination import InfiniteScrollPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class WebProductVideoTypeListView(ListAPIView):
    serializer_class = WebProductVideoTypeSerializer
    pagination_class = InfiniteScrollPagination
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ProductFilter
    search_fields = ['product__name']

    def get_queryset(self):
        queryset = ProductVideoType.objects.select_related('product').annotate(
            comment_count=Count('product__product_comment')
        )
        return queryset


class UserWebProductTypeListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WebProductVideoTypeSerializer
    pagination_class = InfiniteScrollPagination
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ProductFilter
    search_fields = ['product__name']

    def get_queryset(self):
        return ProductVideoType.objects.filter(product__user=self.request.user)


class ChannelWebProductTypeListView(ListAPIView):
    serializer_class = WebProductVideoTypeSerializer
    pagination_class = InfiniteScrollPagination
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ProductFilter
    search_fields = ['product__name']

    def get_queryset(self):
        return ProductVideoType.objects.filter(product__user__username=self.kwargs['username'])


class WebUploadProductCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = WebUploadProductCREATESerializer


class WebUploadProductUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = WebUploadProductUPDATESerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        product_instance = self.get_object()

        if product_instance.user != request.user:
            return Response("You don't have permission to update this product.", status=status.HTTP_403_FORBIDDEN)

        product_serializer = self.get_serializer(
            product_instance, data=request.data, partial=True)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response(product_serializer.data)


class WebProductDeleteAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = WebUploadProductCREATESerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        product = self.get_object()

        if product.user != request.user:
            return Response({"detail": "You do not have permission to delete this product."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShortsDeleteAPIView(DestroyAPIView):
    queryset = ProductVideoType.objects.filter(product_type='Shorts')
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        shorts = self.get_object()

        if shorts.product.user != request.user:
            return Response({"detail": "You do not have permission to delete this shorts."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(shorts)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProductLikeWebAPIView(ListAPIView):
    queryset = ProductVideoType.objects.all()
    serializer_class = WebProductVideoTypeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = InfiniteScrollPagination

    def get_queryset(self):
        user = self.request.user
        product_type = self.request.GET.get('product_type')
        liked_product_ids = UserProductLike.objects.filter(
            user=user).values_list('product__id', flat=True)
        if product_type:
            return ProductVideoType.objects.filter(
                product_id__in=liked_product_ids,
                product_type=product_type
            )
        return ProductVideoType.objects.filter(
            product_id__in=liked_product_ids
        )


class TrendingAPIView(ListAPIView):
    queryset = ProductVideoType.objects.select_related('product').all()
    serializer_class = WebProductVideoTypeSerializer
    pagination_class = InfiniteScrollPagination
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    ordering_fields = ['product__view_count']
    ordering = ['-product__view_count']

    def get_queryset(self):
        product_type = self.request.GET.get('product_type')
        if product_type:
            return ProductVideoType.objects.filter(
                product_type=product_type
            )
        return self.queryset


class UpdateProductPremiumView(UpdateAPIView):
    serializer_class = ProductPremiumUpdateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_ids = serializer.validated_data.get('product_ids')
        updated_count = Product.objects.filter(
            id__in=product_ids).update(is_premium=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
