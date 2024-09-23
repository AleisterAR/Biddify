from django.shortcuts import render
from item.models import Item, Category

# Create your views here.
def inventory(request):
    condition_choices = Item.CONDITION_TYPES
    return render(request, "items/inventory.html", {"condition_choices":condition_choices})