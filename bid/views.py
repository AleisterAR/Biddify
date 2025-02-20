from django.shortcuts import render, redirect
from bid.forms import AuctionForm
from bid.models import Auction, Notification, Bid
from item.models import Item, ItemImage
from django.contrib import messages
import json
from django_htmx.http import trigger_client_event
from django.http import HttpResponse
from django.db.models import Q, Max, F, OuterRef, Subquery

# Create your views here.
def create_auction(request, item_id):
    item = Item.objects.get(id=item_id)
    if request.method == 'POST':
        form = AuctionForm(data=request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.item = item
            auction.save()
            messages.success(request, "Auction has been registered successfully!")
            response = render(request, 'items/partials/start_auction_partial.html', {'form': form, 'item': item})
            response["HX-Trigger"] = "auction_created"
            return response
    else:
        form = AuctionForm()
    return render(request, 'items/partials/start_auction_partial.html', {'form': form, 'item': item})

def delete_notification(request, notification_message):
    Notification.objects.get(message=notification_message, user=request.user).delete()
    noti_count = Notification.objects.filter(user=request.user).count()
    if noti_count > 0:
        return HttpResponse("")
    return render(request, 'utilities/partials/empty_notification.html')

def delete_all_notifications(request):
    Notification.objects.filter(user=request.user).delete()
    return render(request, 'utilities/partials/empty_notification.html', context={"has_unread":False}) 

def mark_as_read(request, notification_message):
    new_noti = Notification.objects.get(message=notification_message, user=request.user)
    new_noti.is_read = True
    new_noti.save()
    has_unread = Notification.objects.filter(user=request.user, is_read=False).count() > 0
    return render(request, 'utilities/partials/read_notification.html', context={"notification": new_noti, "has_unread": has_unread})

def feature_auctions(request):
    first_images = ItemImage.objects.filter(item=OuterRef('item_id')).values('image')[:1]
    auctions = Auction.objects.prefetch_related('bids').annotate(max_bid = Max('bids__bid_amount'), first_image=Subquery(first_images)).exclude(max_bid=None).order_by('-max_bid')

    return render(request, 'utilities/partials/featured_auctions.html', context={'featured_auctions':auctions})