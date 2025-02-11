from django.db import models
from item.models import Item
from participants.models import Participant
from django.utils import timezone

# Create your models here.
class Auction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="auction")
    starting_time = models.DateTimeField(null=True, blank=True)
    ending_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Auction for {self.item.name}'
    
    def timer_started(self):
        return timezone.now() >= self.starting_time
    
    def auction_ended(self):
        return timezone.now() > self.ending_time
    
class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(Participant, on_delete=models.CASCADE)
    bid_amount = models.PositiveSmallIntegerField()
    bid_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Bid by {self.bidder.first_name} {self.bidder.last_name} on {self.auction.item.name}'

class Notification(models.Model):
    message = models.TextField(null=True, blank=True)
    user = models.ForeignKey(Participant, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)