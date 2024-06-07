import django_filters.rest_framework
from rest_framework import filters, status
from django.db.models import Count
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from product.filters import ProductFilter
from product.models import Product, ProductVideoType
from product.serializers import WebProductVideoTypeSerializer, WebUploadProductCREATESerializer
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


class WebUploadProductCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = WebUploadProductCREATESerializer


# class WebUploadProductUpdateView(UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Product.objects.all()
#     serializer_class = WebUploadProductUPDATESerializer
#     lookup_field = 'pk'


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
