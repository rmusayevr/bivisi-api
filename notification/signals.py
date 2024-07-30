from django.dispatch import receiver, Signal
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from notification.models import Notification

# Define signals
video_liked = Signal(providing_args=['user', 'video'])
comment_added = Signal(providing_args=['user', 'video', 'comment'])
chat_message_sent = Signal(providing_args=['user', 'chat', 'message'])


# Signal handlers
@receiver(video_liked)
def video_liked_handler(sender, **kwargs):
    user = kwargs['user']
    video = kwargs['video']
    message = f"{user.username} liked your video '{video.title}'."
    send_notification(user, message, event_type='video_liked')


@receiver(comment_added)
def comment_added_handler(sender, **kwargs):
    user = kwargs['user']
    video = kwargs['video']
    comment = kwargs['comment']
    message = f"{user.username} commented on your video '{video.title}': {comment.text}"
    send_notification(user, message, event_type='comment_added')


@receiver(chat_message_sent)
def chat_message_sent_handler(sender, **kwargs):
    user = kwargs['user']
    chat = kwargs['chat']
    message = kwargs['message']
    notification_message = f"{user.username} sent a message in chat '{chat.name}': {message.text}"
    send_notification(user, notification_message, event_type='chat_message_sent')


# Function to send notifications
def send_notification(user, message, event_type):
    notification = Notification.objects.create(recipient=user, message=message)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {
            "type": "send_notification",
            "message": message,
            "event_type": event_type,
        }
    )
