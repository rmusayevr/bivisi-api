from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from notification.firebase_manager import send_notification
from notification.models import Notification
from product.models import Product, ProductComment, ProductCommentLike, UserProductLike
from services.notification_channel import trigger_notification


class ToggleProductLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_id)
        user_like, created = UserProductLike.objects.get_or_create(
            user=self.request.user)
        
        notification = None

        if product in user_like.product.all():
            user_like.product.remove(product)
            product.like_count -= 1
            product.save()
            message = "Product unliked"
            status_code = status.HTTP_204_NO_CONTENT
        else:
            user_like.product.add(product)
            product.like_count += 1
            product.save()
            # Create a new notification
            notification = Notification.objects.create(
                recipient=product.user,  # Assuming the Product model has an "owner" field
                sender=self.request.user,
                message=f"{self.request.user.username} liked your product.",
                notification_type=Notification.NotificationTypeChoices.LIKE,
                product_id=product
            )
            trigger_notification(notification)
            send_notification("Product Like", notification.message, notification.recipient.token)

            message = "Product liked"
            status_code = status.HTTP_201_CREATED

        response_data = {"message": message}
        if notification:
            response_data.update({
                "message": notification.message,
                "notification_id": notification.pk,
                "notification_type": notification.notification_type,
                "product_id": notification.product_id.pk,
                "product_cover_image": notification.product_id.product_video_type.first().cover_image.url,
                "sender": {
                    "first_name": notification.sender.first_name,
                    "last_name": notification.sender.last_name,
                    "username": notification.sender.username,
                    "avatar": notification.sender.avatar.url if notification.sender.avatar else None,
                },
            })
        return Response(response_data, status=status_code)


class ToggleProductCommentLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_comment_id, *args, **kwargs):
        product_comment = get_object_or_404(
            ProductComment, pk=product_comment_id)
        user_like, created = ProductCommentLike.objects.get_or_create(
            user=self.request.user)
        
        notification = None

        if product_comment in user_like.product_comment.all():
            user_like.product_comment.remove(product_comment)
            product_comment.like_count -= 1
            product_comment.save()
            message = "Product comment unliked"
            status_code = status.HTTP_204_NO_CONTENT
        else:
            user_like.product_comment.add(product_comment)
            product_comment.like_count += 1
            product_comment.save()
            # Create a new notification
            notification = Notification.objects.create(
                # Assuming the ProductComment model has a "user" field
                recipient=product_comment.user,
                sender=self.request.user,
                message=f"{self.request.user.username} liked your comment.",
                notification_type=Notification.NotificationTypeChoices.LIKE,
                # Assuming ProductComment has a foreign key to Product
                product_id=product_comment.product
            )
            trigger_notification(notification)
            send_notification("Comment Like", notification.message, notification.recipient.token)
            message = "Product comment liked"
            status_code = status.HTTP_201_CREATED

        response_data = {"message": message}
        if notification:
            response_data.update({
                "message": notification.message,
                "notification_id": notification.pk,
                "notification_type": notification.notification_type,
                "product_id": notification.product_id.pk,
                "product_cover_image": notification.product_id.product_video_type.first().cover_image.url,
                "sender": {
                    "first_name": notification.sender.first_name,
                    "last_name": notification.sender.last_name,
                    "username": notification.sender.username,
                    "avatar": notification.sender.avatar.url if notification.sender.avatar else None,
                },
            })
        return Response(response_data, status=status_code)
