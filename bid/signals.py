from bid.models import Bid, Notification
from participants.models import Participant
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Bid)
def send_bid_notification(sender, instance, created, **kwargs):
    if created:
        notifications = []
        auction_title = instance.auction.item.name
        channel_layer = get_channel_layer()
        participants = Participant.objects.filter(bid__auction=instance.auction).distinct()
        for participant in participants:
            if participant.id != instance.bidder.id:
                notification_message = f"{instance.bidder.username} bid € {instance.bid_amount} on {auction_title}."
                notification = Notification(message=notification_message, user=participant)
                notifications.append(notification)
                async_to_sync(channel_layer.group_send)(
                    f"user_{participant.id}_notifications", {
                        "type": "send_notification",
                        "notification_data": {
                            "notification" : notification
                        }
                    }
                )
        news = Notification.objects.bulk_create(notifications)