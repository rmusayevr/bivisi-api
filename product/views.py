from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import CategorySerializer, ProductCREATESerializer, ProductCommentCREATESerializer, ProductCommentLikeCREATESerializer, ProductCommentLikeREADSerializer, ProductCommentREADSerializer, ProductREADSerializer, UserProductLikeCREATESerializer, UserProductLikeREADSerializer
from .models import Category, Product, ProductComment, ProductCommentLike, UserProductLike



class GenericAPIViewSerializerMixin:
    def get_serializer_class(self):
        return self.serializer_classes[self.request.method]


# Category GET & POST
class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    serializer_class = CategorySerializer

# Category GET & PUT & PATCH & DELETE
class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Product GET & POST
class ProductListCreateAPIView(GenericAPIViewSerializerMixin, ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_classes = {
        'GET' : ProductREADSerializer,
        'POST' : ProductCREATESerializer
    }

# Product GET & PUT & PATCH & DELETE
class ProductRetrieveUpdateDestroyAPIView(GenericAPIViewSerializerMixin, RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_classes = {
        'GET' : ProductREADSerializer,
        'PUT' : ProductCREATESerializer,
        'PATCH' : ProductCREATESerializer
    }


# User Product Like GET & POST
class UserProductLikeListCreateAPIView(GenericAPIViewSerializerMixin, ListCreateAPIView):
    queryset = UserProductLike.objects.all()
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
