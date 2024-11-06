from django.urls import path
from bid.views import create_auction

urlpatterns = [
    path("create_auction/<int:item_id>", create_auction, name="create_auction"),
]