from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import datetime
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from bid.models import Auction, Bid
from bid.forms import BidForm, AuctionForm
import json
import asyncio
from participants.models import Participant
from django.template.loader import render_to_string
from participants.models import Participant

class AuctionConsumer(WebsocketConsumer):
    def connect(self):
        self.auction_id = self.scope['url_route']['kwargs']['auction_id']
        self.room_group_name = f"auction_{self.auction_id}"
        self.auction =  Auction.objects.prefetch_related('bids').select_related('item').get(id=self.auction_id)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, 
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        bid_amount = data.get("bid_amount")
        user_id = data.get("user_id")
        user = Participant.objects.get(id=user_id)
        form = BidForm(data={"bid_amount": bid_amount, "auction": self.auction})
        event = {
            "type":"bid_handler",
            "bid_form" : form,
            "success" : False,
            "user": user,
        }
        if status:= form.is_valid():
            bid = Bid.objects.create(auction=self.auction, bidder=user, bid_amount=bid_amount, bid_time=timezone.now())
            event["bid"] = bid
            event["success"] = status
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, event
        )

    def bid_handler(self, event):
        bids = Bid.objects.filter(auction=self.auction).order_by('-bid_time', '-bid_amount')
        context = {"item":self.auction.item, 
         'images': self.auction.item.itemimage_set.all(), 
         "ownership": event["user"] == self.auction.item.owner, 
         "auction_started":True, 
         "auction_created":True, 
         "form": AuctionForm(), 
         "bid_form": event['bid_form'],}
        if event["success"]:
            context['latest_bids'] = bids[:3]
            context['more_bids'] = bids[3:]
        html = render_to_string("items/partials/bidding_history_partial.html", context=context)
        self.send(text_data=html)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.group_name = f"user_{self.user_id}_notifications"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        html = render_to_string("utilities/partials/notification.html", context=event["notification_data"])
        await self.send(text_data=html) 