from django.urls import path
from .views import inventory, item_list

urlpatterns = [
    path('inventory/',inventory,name="inventory"),
    path('item_list/',item_list,name="item_list" )
]