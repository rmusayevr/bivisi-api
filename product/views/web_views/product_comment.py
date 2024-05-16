import django_filters.rest_framework
from rest_framework import filters
from rest_framework.generics import ListAPIView
from product.models import ProductComment
from product.serializers import WebProductCommentSerializer
from services.pagination import InfiniteScrollPagination


# Product Comments only parent comment null
class ParentCommentListAPIView(ListAPIView):
    serializer_class = WebProductCommentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user']
    search_fields = ['comment']
    pagination_class = InfiniteScrollPagination

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductComment.objects.filter(
                    parent_comment__isnull=True,
                    product__id=product_id
                ).select_related(
                    'user'
                )


class SubCommentListAPIView(ListAPIView):
    serializer_class = WebProductCommentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user']
    search_fields = ['comment']
    pagination_class = InfiniteScrollPagination

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        parent_comment_id = self.kwargs['parent_comment_id']
        return  ProductComment.objects.filter(
                    parent_comment__id=parent_comment_id,
                    product__id=product_id
                ).select_related(
                    'user'
                )