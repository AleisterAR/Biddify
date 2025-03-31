from django.urls import path
from bid.views import create_auction, delete_notification, delete_all_notifications, mark_as_read, feature_auctions, auctions

urlpatterns = [
    path("create_auction/<int:item_id>", create_auction, name="create_auction"),
    path("delete_notification/<str:notification_message>", delete_notification, name="delete_notification"),
    path("delete_all_notifications", delete_all_notifications, name="delete_all_notifications"),
    path("mark_as_read/<str:notification_message>", mark_as_read, name="mark_as_read"),
    path("featured_auctions", feature_auctions, name="featured_auctions"),
    path("", auctions, name="auctions")
]