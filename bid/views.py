from django.shortcuts import render, redirect
from bid.forms import AuctionForm
from bid.models import Auction, Notification, Bid
from item.models import Item, ItemImage, Category
from django.contrib import messages
import json
from django_htmx.http import trigger_client_event
from django.http import HttpResponse
from django.db.models import Q, Max, F, OuterRef, Subquery
from django.utils import timezone
from django.core.paginator import Paginator

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
    auctions = Auction.objects.prefetch_related('bids').annotate(max_bid = Max('bids__bid_amount'), first_image=Subquery(first_images)).exclude(max_bid=None, ending_time__lte=timezone.now()).order_by('-max_bid')

    return render(request, 'utilities/partials/featured_auctions.html', context={'featured_auctions':auctions})

def auctions(request):
    search = request.GET.get("search","")
    filter_category = request.GET.get("filter_category","")
    filter_country = request.GET.get("filter_country", "")
    filter_condition = request.GET.get("filter_condition", "")
    first_images = ItemImage.objects.filter(item=OuterRef('id')).values('image')[:1]
    auctions = Item.objects.filter(auction__starting_time__lte=timezone.now(), auction__ending_time__gte=timezone.now()).annotate(highest_bid=Max('auction__bids__bid_amount'), first_image=Subquery(first_images), auction_ending_time=F('auction__ending_time'))
    filters = Q()
    if search:
        filters &= Q(name__icontains=search)
    if filter_category:
        filters &= Q(category__category=filter_category)
    if filter_country:
        filters &= Q(country=filter_country)
    if filter_condition:
        filters &= Q(condition=filter_condition)
    auctions = auctions.filter(filters)
    paginator = Paginator(auctions, 16)
    page = request.GET.get("page")
    auctions = paginator.get_page(page)
    if request.htmx:
        return render(request, 'auctions/partials/auctions_partial.html', {'auctions':auctions})
    condition_choices = Item.CONDITION_TYPES
    categories = Category.objects.all()
    countries = Item.COUNTRY_CHOICES
    return render(request, 'auctions/auctions.html', context={'auctions':auctions, 'categories':categories, 'conditions':condition_choices, 'countries':countries})