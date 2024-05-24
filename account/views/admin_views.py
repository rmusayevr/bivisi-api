from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from services.pagination import InfiniteScrollPagination
from ..models import ChannelCategory, PhoneNumber, Subscription
from ..serializers import (
    ChannelCategorySerializer,
    SubscriptionReadSerializer,
    SubscriptionCreateSerializer,
    PhoneNumberReadSerializer,
    PhoneNumberCreateSerializer
)


class GenericAPIViewSerializerMixin:
    def get_serializer_class(self):
        return self.serializer_classes[self.request.method]


# Subscription GET & POST
class SubscriptionListCreateAPIView(GenericAPIViewSerializerMixin, ListCreateAPIView):
    queryset = Subscription.objects.all()
    pagination_class = InfiniteScrollPagination
    serializer_classes = {
        'GET': SubscriptionReadSerializer,
        'POST': SubscriptionCreateSerializer
    }

# Subscription GET & PUT & PATCH & DELETE
class SubscriptionRetrieveUpdateDestroyAPIView(GenericAPIViewSerializerMixin, RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_classes = {
        'GET': SubscriptionReadSerializer,
        'PUT': SubscriptionCreateSerializer,
        'PATCH': SubscriptionCreateSerializer,
        'DELETE': SubscriptionCreateSerializer,
    }

# Phone Number GET & POST
class PhoneNumberListCreateAPIView(GenericAPIViewSerializerMixin, ListCreateAPIView):
    queryset = PhoneNumber.objects.all()
    pagination_class = InfiniteScrollPagination
    serializer_classes = {
        'GET': PhoneNumberReadSerializer,
        'POST': PhoneNumberCreateSerializer
    }

# Phone Number GET & PUT & PATCH & DELETE
class PhoneNumberRetrieveUpdateDestroyAPIView(GenericAPIViewSerializerMixin, RetrieveUpdateDestroyAPIView):
    queryset = PhoneNumber.objects.all()
    serializer_classes = {
        'GET': PhoneNumberReadSerializer,
        'PUT': PhoneNumberCreateSerializer,
        'PATCH': PhoneNumberCreateSerializer,
        'DELETE': PhoneNumberCreateSerializer,
    }

# ChannelCategory GET & POST
class ChannelCategoryListCreateAPIView(GenericAPIViewSerializerMixin, ListCreateAPIView):
    queryset = ChannelCategory.objects.all()
    pagination_class = InfiniteScrollPagination
    serializer_classes = {
        'GET': ChannelCategorySerializer,
        'POST': ChannelCategorySerializer
    }

# ChannelCategory GET & PUT & PATCH & DELETE
class ChannelCategoryRetrieveUpdateDestroyAPIView(GenericAPIViewSerializerMixin, RetrieveUpdateDestroyAPIView):
    queryset = ChannelCategory.objects.all()
    serializer_classes = {
        'GET': ChannelCategorySerializer,
        'PUT': ChannelCategorySerializer,
        'PATCH': ChannelCategorySerializer,
        'DELETE': ChannelCategorySerializer,
    }
