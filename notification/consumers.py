import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        notification_data = {
            "message": data["message"],
            "notification_id": data["notification_id"],
            "notification_type": data["notification_type"],
            "product_cover_image": data["product_cover_image"],
            "sender": data["sender"],
        }
        await self.send(text_data=json.dumps(notification_data))

    async def send_notification(self, event):
        notification_data = {
            "message": event["message"],
            "notification_id": event["notification_id"],
            "notification_type": event["notification_type"],
            "product_id": event.get("product_id", None),
            "product_cover_image": event["product_cover_image"],
            "sender": event["sender"],
        }
        await self.send(text_data=json.dumps(notification_data))
