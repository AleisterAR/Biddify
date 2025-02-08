from django.contrib import admin
from bid.models import Auction, Bid, Notification
# Register your models here.
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Notification)