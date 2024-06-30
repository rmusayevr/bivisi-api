import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from notification.models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            # Create group name based on user ID or other criteria
            group_name = f"notifications_{user.id}"
            await self.channel_layer.group_add(group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()  # Close connection if not authenticated

    async def disconnect(self, close_code):
        user = self.scope['user']
        if user.is_authenticated:
            group_name = f"notifications_{user.id}"
            await self.channel_layer.group_discard(group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            # Validate data (optional, based on your notification format)
            # ...
        except json.JSONDecodeError:
            # Handle invalid JSON data gracefully (e.g., log error)
            return

        # Extract relevant information from data
        notification_id = data.get('notification_id')
        # ... other relevant fields

        # Fetch notification from database (if needed)
        notification = None
        if notification_id:
            try:
                notification = Notification.objects.get(pk=notification_id)
            except Notification.DoesNotExist:
                # Handle non-existent notification (e.g., log error)
                pass

        # Perform actions based on received data (optional)
        # ... (e.g., mark notification as read)

    async def send_notification(self, event):
        notification_data = event.get('value')
        await self.send(text_data=notification_data)
