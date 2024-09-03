from django.db import models
from item.models import Item
from participants.models import Participant
from django.utils import timezone

# Create your models here.
class Auction(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    starting_time = models.DateTimeField()
    ending_time = models.DateTimeField()

    def __str__(self):
        return f'Auction for {self.item.name}'
    
class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(Participant, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Bid by {self.bidder.first_name} {self.bidder.last_name} on {self.auction.item.name}'
