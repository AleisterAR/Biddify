from bid.models import Bid, Auction
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer

@receiver(post_save, sender=Bid)
def send_bid_notification(sender, instance, created, **kwargs):
    if created:
        pass