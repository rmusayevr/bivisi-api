from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from services.pagination import InfiniteScrollPagination
from ..models import Wishlist, BasketItem, Basket
from ..serializers import (
    WishlistReadSerializer,
    WishlistCreateSerializer,
    BasketItemReadSerializer,
    BasketItemCreateSerializer,
    BasketReadSerializer,
    BasketCreateSerializer
)


class GenericAPIViewSerializerMixin:
    def get_serializer_class(self):
        return self.serializer_classes[self.request.method]


# Wishlist GET & POST
class WishlistListCreateAPIView(GenericAPIViewSerializerMixin, ListCreateAPIView):
    queryset = Wishlist.objects.all()
    pagination_class = InfiniteScrollPagination
    serializer_classes = {
        'GET': WishlistReadSerializer,
        'POST': WishlistCreateSerializer
    }


# Wishlist GET & PUT & PATCH & DELETE
class WishlistRetrieveUpdateDestroyAPIView(GenericAPIViewSerializerMixin, RetrieveUpdateDestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_classes = {
        'GET': WishlistReadSerializer,
        'PUT': WishlistCreateSerializer,
        'PATCH': WishlistCreateSerializer,
        'DELETE': WishlistCreateSerializer,
    }


# BasketItem GET & POST
class BasketItemListCreateAPIView(GenericAPIViewSerializerMixin, ListCreateAPIView):
    queryset = BasketItem.objects.all()
    pagination_class = InfiniteScrollPagination
    serializer_classes = {
        'GET': BasketItemReadSerializer,
        'POST': BasketItemCreateSerializer
    }


# BasketItem GET & PUT & PATCH & DELETE
class BasketItemRetrieveUpdateDestroyAPIView(GenericAPIViewSerializerMixin, RetrieveUpdateDestroyAPIView):
    queryset = BasketItem.objects.all()
    serializer_classes = {
        'GET': BasketItemReadSerializer,
        'PUT': BasketItemCreateSerializer,
        'PATCH': BasketItemCreateSerializer,
        'DELETE': BasketItemCreateSerializer,
    }


# Basket GET & POST
class BasketListCreateAPIView(GenericAPIViewSerializerMixin, ListCreateAPIView):
    queryset = Basket.objects.all()
    pagination_class = InfiniteScrollPagination
    serializer_classes = {
        'GET': BasketReadSerializer,
        'POST': BasketCreateSerializer
    }


# Basket GET & PUT & PATCH & DELETE
class BasketRetrieveUpdateDestroyAPIView(GenericAPIViewSerializerMixin, RetrieveUpdateDestroyAPIView):
    queryset = Basket.objects.all()
    serializer_classes = {
        'GET': BasketReadSerializer,
        'PUT': BasketCreateSerializer,
        'PATCH': BasketCreateSerializer,
        'DELETE': BasketCreateSerializer,
    }
