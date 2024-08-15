from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from services.pagination import InfiniteScrollPagination
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListCreateView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = InfiniteScrollPagination

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).select_related(
            "sender", "product_id", "comment_id"
        )


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
