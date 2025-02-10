from bid.models import Notification

def notification_processor(request):
    notifications, has_unread = [], False
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
        has_unread = notifications.filter(is_read=False).count() > 0
    else:
        notifications = []
    return {"notifications": notifications, "has_unread": has_unread}