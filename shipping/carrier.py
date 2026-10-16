"""
Mock shipping carrier.

Nothing here talks to a real carrier: tracking numbers are random and the parcel
"moves" purely based on how much time has passed since it was shipped. Each
transit step takes MOCK_SHIPPING_STEP_SECONDS (half that for express), so a
parcel goes shipped -> in transit -> out for delivery -> delivered in a few
minutes, which is handy for demos.
"""
import random
import string
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from shipping.models import Shipment, ShipmentEvent
from shipping.notifications import notify

CARRIER_NAME = "Biddify Express"
ORIGIN_LOCATION = "Biddify Warehouse, Amsterdam"
SORTING_HUBS = ["Amsterdam, NL", "Frankfurt, DE", "Paris, FR", "Brussels, BE", "Milan, IT", "Vienna, AT"]
TRANSIT_FLOW = ['shipped', 'in_transit', 'out_for_delivery', 'delivered']
DELIVERY_DAYS = {'standard': 5, 'express': 2}


def generate_tracking_number():
    while True:
        tracking_number = "BDF" + "".join(random.choices(string.digits, k=10)) + "EU"
        if not Shipment.objects.filter(tracking_number=tracking_number).exists():
            return tracking_number


def step_seconds(shipment):
    seconds = getattr(settings, "MOCK_SHIPPING_STEP_SECONDS", 120)
    return seconds / 2 if shipment.method == 'express' else seconds


def _destination(shipment):
    return ", ".join(part for part in [shipment.city, shipment.country] if part)


def _transit_step(shipment, status):
    hub = random.Random(shipment.tracking_number).choice(SORTING_HUBS)
    steps = {
        'in_transit': ("Arrived at sorting hub", hub),
        'out_for_delivery': ("Out for delivery with courier", _destination(shipment)),
        'delivered': (f"Delivered to {shipment.recipient_name}", _destination(shipment)),
    }
    return steps[status]


def _apply_status(shipment, status, at):
    shipment.status = status
    if status == 'shipped':
        shipment.shipped_at = at
        description, location = "Parcel handed over to carrier", ORIGIN_LOCATION
    else:
        description, location = _transit_step(shipment, status)
    if status == 'delivered':
        shipment.delivered_at = at
    shipment.save()
    ShipmentEvent.objects.create(shipment=shipment, status=status, description=description, location=location, created_at=at)

    item_name = shipment.item.name
    if status == 'shipped':
        notify(shipment.buyer, f"Your {item_name} has been shipped. Tracking number {shipment.tracking_number}.")
    elif status == 'out_for_delivery':
        notify(shipment.buyer, f"Your {item_name} is out for delivery today.")
    elif status == 'delivered':
        notify(shipment.buyer, f"Your {item_name} has been delivered. Enjoy!")
        if shipment.seller:
            notify(shipment.seller, f"{item_name} was delivered to {shipment.buyer.username}.")


def create_label(shipment):
    """Called once the buyer has submitted their address."""
    now = timezone.now()
    shipment.carrier = CARRIER_NAME
    shipment.tracking_number = generate_tracking_number()
    shipment.status = 'label_created'
    shipment.estimated_delivery = timezone.localdate() + timedelta(days=DELIVERY_DAYS[shipment.method])
    shipment.save()
    ShipmentEvent.objects.create(
        shipment=shipment, status='label_created', created_at=now,
        description="Shipping label created, waiting for the seller to hand over the parcel",
        location=ORIGIN_LOCATION,
    )
    if shipment.seller:
        notify(shipment.seller, f"{shipment.buyer.username} added a shipping address for {shipment.item.name}. Please ship it.")
    return shipment


def mark_shipped(shipment):
    _apply_status(shipment, 'shipped', timezone.now())
    return shipment


def sync(shipment):
    """Advance an in-flight shipment according to how much time has passed since it shipped."""
    if shipment.status not in TRANSIT_FLOW[:-1] or not shipment.shipped_at:
        return shipment
    step = step_seconds(shipment)
    elapsed = (timezone.now() - shipment.shipped_at).total_seconds()
    steps_due = min(int(elapsed // step), len(TRANSIT_FLOW) - 1)
    current = TRANSIT_FLOW.index(shipment.status)
    while current < steps_due:
        current += 1
        _apply_status(shipment, TRANSIT_FLOW[current], shipment.shipped_at + timedelta(seconds=step * current))
    return shipment


def advance(shipment):
    """Force the next status right now (demo helper)."""
    if shipment.status == 'label_created':
        return mark_shipped(shipment)
    if shipment.status in TRANSIT_FLOW[:-1]:
        next_status = TRANSIT_FLOW[TRANSIT_FLOW.index(shipment.status) + 1]
        _apply_status(shipment, next_status, timezone.now())
    return shipment
