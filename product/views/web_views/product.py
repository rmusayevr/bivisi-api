import django_filters.rest_framework
from rest_framework import filters
from django.db.models import Count
from rest_framework.generics import ListAPIView
from product.models import Product, ProductVideoType
from services.pagination import InfiniteScrollPagination
from product.serializers import ProductForTypeSerializer, WebProductVideoTypeSerializer



class WebProductVideoTypeListView(ListAPIView):
    serializer_class = WebProductVideoTypeSerializer
    pagination_class = InfiniteScrollPagination
    # queryset = ProductVideoType.objects.select_related('product').all()  # Use select_related to optimize the query
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product', 'product_type', 'product__category']
    ordering_fields = ['created_at']  # Specify fields allowed to be ordered
    ordering = ['-created_at']

    def get_queryset(self):
        # Annotate the queryset with the comment count for each product
        queryset = ProductVideoType.objects.select_related('product').annotate(
            comment_count=Count('product__product_comment')
        )
        return queryset
