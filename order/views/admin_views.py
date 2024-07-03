from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from services.pagination import InfiniteScrollPagination
from ..models import BasketItem, Basket, Favorite, Order
from ..serializers import (
    FavoriteReadSerializer,
    FavoriteCreateSerializer,
    BasketItemReadSerializer,
    BasketItemCreateSerializer,
    BasketReadSerializer,
    BasketCreateSerializer,
    OrderCreateSerializer,
    OrderReadSerializer
)


class GenericAPIViewSerializerMixin:
    def get_serializer_class(self):
        return self.serializer_classes[self.request.method]


# Favorite GET & POST
class FavoriteListCreateAPIView(GenericAPIViewSerializerMixin, ListCreateAPIView):
    queryset = Favorite.objects.all()
    pagination_class = InfiniteScrollPagination
    serializer_classes = {
        'GET': FavoriteReadSerializer,
        'POST': FavoriteCreateSerializer
    }


# Favorite GET & PUT & PATCH & DELETE
class FavoriteRetrieveUpdateDestroyAPIView(GenericAPIViewSerializerMixin, RetrieveUpdateDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_classes = {
        'GET': FavoriteReadSerializer,
        'PUT': FavoriteCreateSerializer,
        'PATCH': FavoriteCreateSerializer,
        'DELETE': FavoriteCreateSerializer,
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

# Order GET & POST
class OrderListCreateAPIView(GenericAPIViewSerializerMixin, ListCreateAPIView):
    queryset = Order.objects.all()
    pagination_class = InfiniteScrollPagination
    serializer_classes = {
        'GET': OrderReadSerializer,
        'POST': OrderCreateSerializer
    }


# Order GET & PUT & PATCH & DELETE
class OrderRetrieveUpdateDestroyAPIView(GenericAPIViewSerializerMixin, RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_classes = {
        'GET': OrderReadSerializer,
        'PUT': OrderCreateSerializer,
        'PATCH': OrderCreateSerializer,
        'DELETE': OrderCreateSerializer,
    }
