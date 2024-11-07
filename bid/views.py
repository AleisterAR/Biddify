from django.shortcuts import render, redirect
from bid.forms import AuctionForm
from bid.models import Auction
from item.models import Item
from django.contrib import messages

# Create your views here.
def create_auction(request, item_id):
    item = Item.objects.get(id=item_id)
    if request.method == 'POST':
        print(request.POST.get('starting_time'))
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.item = item
            auction.save()
            messages.success(request, "Auction has been registered successfully!")
            return render(request, 'items/partials/start_auction_partial.html', {'form': form, 'item': item})
    else:
        form = AuctionForm()
    return render(request, 'items/partials/start_auction_partial.html', {'form': form, 'item': item})