from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# Trigger WebSocket notification
def trigger_notification(notification):
    # Trigger WebSocket notification
    channel_layer = get_channel_layer()
    group_name = f"user_{notification.recipient.id}"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_notification",
            "message": notification.message,
            "notification_type": notification.notification_type,
            "product_id": notification.product_id.pk if notification.product_id else None
        }
    )
