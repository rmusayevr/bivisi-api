import django_filters.rest_framework
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ...models import Category, Product, ProductComment, ProductCommentLike, ProductVideoType, UserProductLike
from services.pagination import InfiniteScrollPagination
from ...serializers import (CategoryCREATESerializer,
                        CategoryREADSerializer,
                        DashboardProductVideoTypeSerializer,
                        ProductCREATESerializer,
                        ProductCommentCREATESerializer,
                        ProductCommentLikeCREATESerializer,
                        ProductCommentLikeREADSerializer,
                        ProductCommentREADSerializer,
                        ProductREADSerializer,
                        UserProductLikeCREATESerializer,
                        UserProductLikeREADSerializer
                        )



class GenericAPIViewSerializerMixin:
    def get_serializer_class(self):
        return self.serializer_classes[self.request.method]


# Category GET & POST
class CategoryListCreateAPIView(GenericAPIViewSerializerMixin, ListCreateAPIView):
    queryset = Category.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = InfiniteScrollPagination
    serializer_classes = {
        'GET' : CategoryREADSerializer,
        'POST' : CategoryCREATESerializer
    }


# Category GET & PUT & PATCH & DELETE
class CategoryRetrieveUpdateDestroyAPIView(GenericAPIViewSerializerMixin, RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_classes = {
        'GET' : CategoryREADSerializer,
        'PUT' : CategoryCREATESerializer,
        'PATCH' : CategoryCREATESerializer
    }


# Product GET & POST
class ProductListCreateAPIView(GenericAPIViewSerializerMixin, ListCreateAPIView):
    queryset = Product.objects.all()
    pagination_class = InfiniteScrollPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name']
    ordering_fields = ['view_count', 'like_count', 'created_at']  # Specify fields allowed to be ordered
    ordering = ['-created_at']
    serializer_classes = {
        'GET' : ProductREADSerializer,
        'POST' : ProductCREATESerializer
    }


# Product GET & PUT & PATCH & DELETE
class ProductRetrieveUpdateDestroyAPIView(GenericAPIViewSerializerMixin, RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    pagination_class = InfiniteScrollPagination
    serializer_classes = {
        'GET' : ProductREADSerializer,
        'PUT' : ProductCREATESerializer,
        'PATCH' : ProductCREATESerializer
    }


# Product Video Type GET & POST
class DashboardProductVideoTypeListCreateAPIView(ListCreateAPIView):
    queryset = ProductVideoType.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product', 'product_type']
    ordering_fields = ['created_at']  # Specify fields allowed to be ordered
    ordering = ['-created_at']
    pagination_class = InfiniteScrollPagination
    serializer_class = DashboardProductVideoTypeSerializer


# Product Video Type GET & PUT & PATCH & DELETE
class DashboardProductVideoTypeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductVideoType.objects.all()
    serializer_class = DashboardProductVideoTypeSerializer


# User Product Like GET & POST
class UserProductLikeListCreateAPIView(GenericAPIViewSerializerMixin, ListCreateAPIView):
    queryset = UserProductLike.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user']
    search_fields = ['name']
    serializer_classes = {
        'GET' : UserProductLikeREADSerializer,
        'POST' : UserProductLikeCREATESerializer
    }


# User Product Like GET & PUT & PATCH & DELETE
class UserProductLikeRetrieveUpdateDestroyAPIView(GenericAPIViewSerializerMixin, RetrieveUpdateDestroyAPIView):
    queryset = UserProductLike.objects.all()
    serializer_classes = {
        'GET' : UserProductLikeREADSerializer,
        'PUT' : UserProductLikeCREATESerializer,
        'PATCH' : UserProductLikeCREATESerializer
    }


# Product Comment GET & POST
class ProductCommentListCreateAPIView(GenericAPIViewSerializerMixin, ListCreateAPIView):
    queryset = ProductComment.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user']
    search_fields = ['comment']
    pagination_class = InfiniteScrollPagination
    serializer_classes = {
        'GET' : ProductCommentREADSerializer,
        'POST' : ProductCommentCREATESerializer
    }


# Product Comment GET & PUT & PATCH & DELETE
class ProductCommentRetrieveUpdateDestroyAPIView(GenericAPIViewSerializerMixin, RetrieveUpdateDestroyAPIView):
    queryset = ProductComment.objects.all()
    serializer_classes = {
        'GET' : ProductCommentREADSerializer,
        'PUT' : ProductCommentCREATESerializer,
        'PATCH' : ProductCommentCREATESerializer
    }


# User Product Like GET & POST
class ProductCommentLikeListCreateAPIView(GenericAPIViewSerializerMixin, ListCreateAPIView):
    queryset = ProductCommentLike.objects.all()
    pagination_class = InfiniteScrollPagination
    serializer_classes = {
        'GET' : ProductCommentLikeREADSerializer,
        'POST' : ProductCommentLikeCREATESerializer
    }


# User Product Like GET & PUT & PATCH & DELETE
class ProductCommentLikeRetrieveUpdateDestroyAPIView(GenericAPIViewSerializerMixin, RetrieveUpdateDestroyAPIView):
    queryset = ProductCommentLike.objects.all()
    serializer_classes = {
        'GET' : ProductCommentLikeREADSerializer,
        'PUT' : ProductCommentLikeCREATESerializer,
        'PATCH' : ProductCommentLikeCREATESerializer
    }
