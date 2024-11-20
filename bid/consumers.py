from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import datetime
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from bid.models import Auction, Bid
import json
import asyncio
from participants.models import Participant
from django.template.loader import render_to_string

class AuctionConsumer(WebsocketConsumer):
    def connect(self):
        self.auction_id = self.scope['url_route']['kwargs']['auction_id']
        self.room_group_name = f"auction_{self.auction_id}"
        self.auction =  Auction.objects.get(id=self.auction_id)
        async_to_sync(self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        ))
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard(
            self.room_group_name, 
            self.channel_name
        ))

    def receive(self, text_data):
        data = json.loads(text_data)
        bid_amount = data.get("bid_amount")
        user_id = data.get("user_id")
        async_to_sync(self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast_message",
                "message": data,
            },
        ))

    def broadcast_message(self, event):
        message = event["message"]
        
        # bid = Bid.objects.create(auction=self.auction, bidder=get_object_or_404(Participant, id=user_id), bid_amount=bid_amount, bid_time=timezone.now())
        context = {
            "bid" : "",
        }
        html = render_to_string("items/partials/bidding_history_partial.html", context=context)
        async_to_sync(self.send(text_data=json.dumps({
            "message": message,
        })))
    