import django_filters.rest_framework
from rest_framework import filters, status
from django.db.models import Count
from django.http import Http404
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
    WebProductVideoTypeSerializer,
    WebUploadProductCREATESerializer,
    WebUploadProductUPDATESerializer,
)
from services.pagination import InfiniteScrollPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class WebProductVideoTypeListView(ListAPIView):
    serializer_class = WebProductVideoTypeSerializer
    pagination_class = InfiniteScrollPagination
    # queryset = ProductVideoType.objects.select_related('product').all()  # Use select_related to optimize the query
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['product', 'product_type', 'product__category']
    filterset_class = ProductFilter
    # ordering_fields = ['created_at']  # Specify fields allowed to be ordered
    # ordering = ['-created_at']

    def get_queryset(self):
        # Annotate the queryset with the comment count for each product
        queryset = ProductVideoType.objects.select_related('product').annotate(
            comment_count=Count('product__product_comment')
        )
        return queryset


class UserWebProductTypeListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WebProductVideoTypeSerializer
    pagination_class = InfiniteScrollPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter

    def get_queryset(self):
        return ProductVideoType.objects.filter(product__user=self.request.user)


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

        product_serializer = self.get_serializer(product_instance, data=request.data, partial=True)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response(product_serializer.data)

class WebProductDeleteAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = WebUploadProductCREATESerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        product = self.get_object()

        # Ensure the product belongs to the requesting user
        if product.user != request.user:
            return Response({"detail": "You do not have permission to delete this product."}, status=status.HTTP_403_FORBIDDEN)

        # Perform the delete operation
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShortsDeleteAPIView(DestroyAPIView):
    queryset = ProductVideoType.objects.filter(product_type='Shorts')
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        shorts = self.get_object()

        # Ensure the shorts belong to a product owned by the requesting user
        if shorts.product.user != request.user:
            return Response({"detail": "You do not have permission to delete this shorts."}, status=status.HTTP_403_FORBIDDEN)

        # Perform the delete operation
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
