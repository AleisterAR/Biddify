from bid.consumers import AuctionConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r"ws/auction/(?P<auction_id>\d+)/$", AuctionConsumer.as_asgi()),
]