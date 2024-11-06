from django.utils import timezone
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from bid.models import Auction
import json
import asyncio

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.auction_id = self.scope['url_route']['kwargs']['auction_id']
        self.room_group_name = f"auction_{self.auction_id}"

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )  
        self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def send_countdown_time(self):
        auction = self.get_auction_data(self.auction_id)
        while True:
            remaining_time = auction.ending_time - timezone.now()
            if auction.starting_time < timezone.now():
                await self.send(text_data=json.dumps({"countdown": "Auction will begin in "}))
            elif remaining_time.total_seconds() <= 0:
                remaining_time = 0
                await self.send(text_data=json.dumps({"countdown": "Auction ended"}))
                break
            else:
                await self.send(
                    text_data=json.dumps(
                        {
                            "countdown": f"{remaining_time.total_seconds()}"
                        }
                    )
                )
                await asyncio.sleep(1)

    @staticmethod
    async def get_auction_data(auction_id):
        return await Auction.objects.filter(id=auction_id).aget()