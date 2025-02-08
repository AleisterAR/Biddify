from bid.consumers import AuctionConsumer, NotificationConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r"ws/auction/(?P<auction_id>\d+)/", AuctionConsumer.as_asgi()),
    re_path(r"ws/notifications/(?P<user_id>\d+)/", NotificationConsumer.as_asgi()),
]