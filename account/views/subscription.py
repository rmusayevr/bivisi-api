from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ..models import User, Subscription
from ..serializers import (
    PopularChannelSerializer,
    SubscriptionReadWebSerializer,
)
from services.pagination import InfiniteScrollPagination


class SubscribeWebAPIView(ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionReadWebSerializer
    pagination_class = InfiniteScrollPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(follower=self.request.user)


class ToggleSubscribeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'delete']

    def post(self, request, pk, *args, **kwargs):
        follower = request.user
        follows = get_object_or_404(User, pk=pk)

        if follower == follows:
            return Response({'error': 'You cannot subscribe to yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        subscription, created = Subscription.objects.get_or_create(
            follower=follower, follows=follows)

        return Response({'status': 'subscribed'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, *args, **kwargs):
        follower = request.user
        follows = get_object_or_404(User, pk=pk)
        try:
            subscription = Subscription.objects.get(
                follower=follower, follows=follows)
            subscription.delete()
            return Response({'status': 'unsubscribed'}, status=status.HTTP_204_NO_CONTENT)
        except Subscription.DoesNotExist:
            return Response({'error': 'Subscription does not exist'}, status=status.HTTP_404_NOT_FOUND)


class PopularChannelsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        popular_channels = User.objects.annotate(
            followers_count=Count('followers')
        ).order_by('-followers_count')[:5]

        serializer = PopularChannelSerializer(popular_channels, many=True)
        return Response(serializer.data)


class SubscriptionsAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = PopularChannelSerializer
    filter_backends = [OrderingFilter]
    pagination_class = InfiniteScrollPagination

    def get_queryset(self):
        subscriptions = User.objects.annotate(
            followers_count=Count('followers')
        )
        subscriptions = subscriptions[:50]
        return subscriptions
