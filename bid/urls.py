from django.urls import path
from bid.views import create_auction, delete_notification

urlpatterns = [
    path("create_auction/<int:item_id>", create_auction, name="create_auction"),
    path("delete_notification/<int:notification_id>", delete_notification, name="delete_notification")
]