from django.shortcuts import render, get_object_or_404
from item.models import Item, Category, ItemImage
from participants.models import Participant
from django.utils import timezone
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q
from bid.models import Auction, Bid
from bid.forms import AuctionForm, BidForm
from django.db.models import OuterRef, Subquery
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def inventory(request):
    owner = get_object_or_404(Participant, id=request.user.id)
    search = request.GET.get("search","")
    filter_category = request.GET.get("filter_category","")
    first_images = ItemImage.objects.filter(item=OuterRef('id')).values('image')[:1]
    items = Item.objects.filter(owner=owner).annotate(first_image=Subquery(first_images))
    filters = Q()
    if search:
        filters &= Q(name__icontains=search)
    if filter_category:
        filters &= Q(category__category=filter_category)
    items = items.filter(filters)
    paginator = Paginator(items, 16)
    page = request.GET.get("page")
    belongings = paginator.get_page(page)
    if request.htmx:
        return render(request, "items/partials/inventory_partial.html", {"belongings": belongings})
    condition_choices = Item.CONDITION_TYPES
    categories = Category.objects.all()
    countries = Item.COUNTRY_CHOICES
    context = {"condition_choices":condition_choices, "categories":categories, "belongings":belongings, "countries":countries}
    return render(request, "items/inventory.html", context=context)

def item_list(request):
    return render(request, "items/item_list.html")

@login_required
def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    images = item.itemimage_set.all()
    ownership = request.user == item.owner
    auction_started = auction_created = False
    context = {"item":item, 'images': images, "ownership":ownership, "auction_started":auction_started, "auction_created":auction_created, "form": AuctionForm(), "bid_form": BidForm()}
    if auction_created := Auction.objects.filter(item=item).exists():
        auction = Auction.objects.filter(item=item)[0]
        bids = Bid.objects.filter(auction=auction).select_related("bidder").order_by('-bid_time', '-bid_amount')
        auction_started = auction.timer_started()
        winner = None
        if auction.auction_ended():
            winner = bids[0].bidder.id if len(bids) != 0 else None
        context["auction"], context["auction_created"], context["auction_started"], context["latest_bids"], context["more_bids"], context['winner'], context["highest_bid"] = auction, auction_created, auction_started, bids[:3], bids[3:], winner, bids[0] if len(bids) != 0 else ""
        return render(request, "items/item_detail.html", context=context)
    return render(request, "items/item_detail.html", context=context)


def add_item(request):
    owner = get_object_or_404(Participant, id=request.user.id)
    images = []
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        condition = request.POST.get('condition')
        year = request.POST.get('year')
        starting_price = request.POST.get('price')
        provenance = request.FILES.get('provenance')
        category_name = request.POST.get('category')
        creator = request.POST.get('creator')
        country = request.POST.get('country')
        item = Item.objects.create(
            name=name,
            description=description,
            category=get_object_or_404(Category, category=category_name),
            condition=condition,
            creator=creator,
            country=country,
            year=year,
            starting_price=starting_price,
            provenance=provenance,
            owner=owner,
            created_at=timezone.now()
        )
        for file in request.FILES.getlist('images[]'):
            images.append(ItemImage(image=file, item=item))
        ItemImage.objects.bulk_create(images)
        return JsonResponse({"status":"success"})

