from django.shortcuts import render, get_object_or_404
from item.models import Item, Category, ItemImage
from participants.models import Participant
from django.utils import timezone
from django.core.paginator import Paginator
from django.conf import settings

# Create your views here.
def inventory(request):
    owner = get_object_or_404(Participant, id=request.user.id)
    search = request.GET.get("search")
    items = Item.objects.filter(owner=owner)
    if search:
        items = Item.objects.filter(owner=owner, name__icontains=search)
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
            ItemImage.objects.create(image=file, item=item)
    paginator = Paginator(items, 16)
    page = request.GET.get("page")
    belongings = paginator.get_page(page)
    if request.htmx:
        return render(request, "items/inventory_partial.html", {"belongings": belongings})
    condition_choices = Item.CONDITION_TYPES
    categories = Category.objects.all()
    countries = Item.COUNTRY_CHOICES
    context = {"condition_choices":condition_choices, "categories":categories, "belongings":belongings, "countries":countries}
    return render(request, "items/inventory.html", context=context)

def item_list(request):
    return render(request, "items/item_list.html")

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    images = item.itemimage_set.all()
    return render(request, "items/item_detail.html", context={"item":item,'images': images,})

def search_item(request):
    search = request.POST.get("search")
    owner = get_object_or_404(Participant, id=request.user.id)
    print(owner)
    if search:
        results = Item.objects.filter(owner=owner, name__icontains=search)
    else:
        results = Item.objects.filter(owner=owner)
    context = {"results":results}
    return render(request, "items/inventory.html", context=context)