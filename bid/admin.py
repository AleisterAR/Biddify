from django.contrib import admin
from bid.models import Auction, Bid, Notification
from django.db.models import Count
from django.db.models.functions import TruncDay
# Register your models here.
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Notification)

