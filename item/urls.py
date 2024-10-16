from django.urls import path
from .views import inventory, item_list, item_detail

urlpatterns = [
    path('inventory/',inventory,name="inventory"),
    path('item_list/',item_list,name="item_list" ),
    path('item/<int:item_id>/', item_detail, name="item_detail")
]