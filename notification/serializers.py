from rest_framework import serializers
from .models import Notification
from user.serializers import UserDetailSerializer

class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserDetailSerializer()
    sender = UserDetailSerializer()
    product_cover_image = serializers.SerializerMethodField()    

    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "sender",
            "message",
            "notification_type",
            "product_id",
            "comment_id",
            "product_cover_image",
            "is_read",
            "created_at"
        ]
        read_only_fields = ["id", "created_at", "recipient", "sender"]

    def get_product_cover_image(self, obj):
        if obj.product_id:
            product_video = obj.product_id.product_video_type.first()
            if product_video and product_video.cover_image:
                return product_video.cover_image.url
        return None
