from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from services.pagination import InfiniteScrollPagination


class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = InfiniteScrollPagination

    def get_queryset(self):
        return self.queryset.filter(recipient=self.request.user)


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(recipient=self.request.user)


class MarkAllAsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        notifications = Notification.objects.filter(
            recipient=user, is_read=False)
        count = notifications.update(is_read=True)
        return Response({'message': f'{count} notifications marked as read.'}, status=status.HTTP_200_OK)
