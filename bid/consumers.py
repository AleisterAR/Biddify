from django.utils import timezone
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from bid.models import Auction
import json
import asyncio

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.accept()

    async def disconnect(self, close_code):
        self.disconnect()
