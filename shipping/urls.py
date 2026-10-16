from django.urls import path
from .views import shipments, shipping_details, track_shipment, mark_shipped, simulate_next

urlpatterns = [
    path("", shipments, name="shipments"),
    path("<int:shipment_id>/details/", shipping_details, name="shipping_details"),
    path("<int:shipment_id>/track/", track_shipment, name="track_shipment"),
    path("<int:shipment_id>/mark_shipped/", mark_shipped, name="mark_shipped"),
    path("<int:shipment_id>/simulate/", simulate_next, name="simulate_shipment"),
]
