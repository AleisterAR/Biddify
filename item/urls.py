from django.urls import path
from .views import inventory

urlpatterns = [
    path('inventory/',inventory,name="inventory"),
]