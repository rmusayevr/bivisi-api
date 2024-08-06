import django_filters.rest_framework
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, DestroyAPIView
from notification.firebase_manager import send_notification
from notification.models import Notification
from product.models import Product, ProductComment, ProductCommentLike
from product.serializers import ProductCommentCREATESerializer, WebProductCommentSerializer
from services.notification_channel import trigger_notification
from services.pagination import InfiniteScrollPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Product Comments only parent comment null
class ParentCommentListAPIView(ListAPIView):
    serializer_class = WebProductCommentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user']
    search_fields = ['comment']
    pagination_class = InfiniteScrollPagination

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductComment.objects.filter(
            parent_comment__isnull=True,
            product__id=product_id
        ).select_related(
            'user'
        )


class SubCommentListAPIView(ListAPIView):
    serializer_class = WebProductCommentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user']
    search_fields = ['comment']
    pagination_class = InfiniteScrollPagination

    def get_queryset(self):
        parent_comment_id = self.kwargs['parent_comment_id']
        return ProductComment.objects.filter(
            parent_comment__id=parent_comment_id,
        ).select_related(
            'user'
        )


class ProductCommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the product', nullable=True),
                'parent_comment': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the parent comment', nullable=True, default=None),
                'comment': openapi.Schema(type=openapi.TYPE_STRING, description='Comment text', nullable=False),
            },
            required=['comment'],
            description="Either 'product' or 'parent_comment' must be provided."
        ),
        responses={
            201: openapi.Response('Created', ProductCommentCREATESerializer),
            400: 'Bad Request'
        }
    )
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = self.request.user.pk

        notification = None

        if 'product' not in data and 'parent_comment' not in data:
            return Response({"detail": "Either product or parent_comment must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductCommentCREATESerializer(data=data)
        if serializer.is_valid():
            comment = serializer.save()

            # Determine the recipient and notification type
            if data['parent_comment']:
                parent_comment = ProductComment.objects.get(
                    pk=data['parent_comment'])
                # Assuming the ProductComment model has a 'user' field
                recipient = parent_comment.user
                message = f"{self.request.user.username} replied to your comment."
                notification_type = Notification.NotificationTypeChoices.COMMENT
            else:
                product = Product.objects.get(pk=data['product'])
                recipient = product.user  # Assuming the Product model has an 'owner' field
                message = f"{self.request.user.username} commented on your product."
                notification_type = Notification.NotificationTypeChoices.COMMENT

            # Create a new notification
            notification = Notification.objects.create(
                recipient=recipient,
                sender=self.request.user,
                message=message,
                notification_type=notification_type,
                # Assuming a foreign key to Product
                product_id=comment.product if 'product' in data else parent_comment.product
            )
            trigger_notification(notification)
            send_notification("Product Comment", notification.message, notification.recipient.token)

            response_data = {'data': serializer.data}
            if notification:
                response_data.update({
                    'message': notification.message,
                    'notification_type': notification.notification_type,
                    'product_id': notification.product_id.pk,
                })
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCommentDeleteView(DestroyAPIView):
    queryset = ProductComment.objects.all()
    serializer_class = WebProductCommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this comment like.")
        super().perform_destroy(instance)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Product comment successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
