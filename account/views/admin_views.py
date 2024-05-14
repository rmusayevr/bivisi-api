from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from services.pagination import InfiniteScrollPagination
from ..models import Subscription
from ..serializers import (
    SubscriptionReadSerializer,
    SubscriptionCreateSerializer
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
