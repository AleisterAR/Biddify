from bid.models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def notify(user, message):
    notification = Notification.objects.create(message=message, user=user, is_read=False)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}_notifications", {
            "type": "send_notification",
            "notification_data": {
                "notification": notification,
                "has_unread": True
            }
        }
    )
    return notification
