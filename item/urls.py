from django.urls import path
from .views import inventory, item_list, item_detail, search_item

urlpatterns = [
    path('inventory/',inventory,name="inventory"),
    path('item_list/',item_list,name="item_list" ),
    path('item/<int:item_id>/', item_detail, name="item_detail"),
    path('search_item/', search_item, name="search_item")
]
