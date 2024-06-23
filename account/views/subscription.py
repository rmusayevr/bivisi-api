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
    SubscriptionSerializer,
)
from services.pagination import InfiniteScrollPagination


class SubscribeWebAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = SubscriptionSerializer
    pagination_class = InfiniteScrollPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        following = Subscription.objects.filter(
            follower=self.request.user).first()

        if not following:
            return User.objects.none()

        return User.objects.filter(id=following.follows.id)


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


class PopularChannelsAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = SubscriptionSerializer
    pagination_class = InfiniteScrollPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['follower_count']

    def get_queryset(self):
        return User.objects.annotate(follower_count=Count('followers')).order_by('-follower_count')


class SubscriptionsAPIView(ListAPIView):
    queryset = User.objects.filter(status="Active")
    serializer_class = SubscriptionSerializer
    filter_backends = [OrderingFilter]
    pagination_class = InfiniteScrollPagination
