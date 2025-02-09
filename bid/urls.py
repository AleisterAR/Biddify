from django.urls import path
from bid.views import create_auction, delete_notification, delete_all_notifications

urlpatterns = [
    path("create_auction/<int:item_id>", create_auction, name="create_auction"),
    path("delete_notification/<str:notification_message>", delete_notification, name="delete_notification"),
    path("delete_all_notifications", delete_all_notifications, name="delete_all_notifications")
]