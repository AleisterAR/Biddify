from django.shortcuts import render, get_object_or_404
from item.models import Item, Category, ItemImage
from participants.models import Participant
from django.utils import timezone

# Create your views here.
def inventory(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        condition = request.POST.get('condition')
        year = request.POST.get('year')
        starting_price = request.POST.get('price')
        provenance = request.FILES.get('provenance')
        category_name = request.POST.get('category')
        owner = get_object_or_404(Participant, id=request.user.id)
        creator = request.POST.get('creator')
        item = Item.objects.create(
            name=name,
            description=description,
            category=get_object_or_404(Category, category=category_name),
            condition=condition,
            creator=creator,
            year=year,
            starting_price=starting_price,
            provenance=provenance,
            owner=owner,
            created_at=timezone.now()
        )
        for file in request.FILES.getlist('images[]'):
            ItemImage.objects.create(image=file, item=item)
        
    condition_choices = Item.CONDITION_TYPES
    categories = Category.objects.all()
    belongings = Item.objects.filter(owner=get_object_or_404(Participant, id=request.user.id))
    context = {"condition_choices":condition_choices, "categories":categories, "belongings":belongings}
    return render(request, "items/inventory.html", context=context)

def item_list(request):
    return render(request, "items/item_list.html")