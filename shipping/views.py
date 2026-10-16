from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from django.conf import settings
from django.db.models import Q
from item.models import ItemImage
from shipping.models import Shipment
from shipping.forms import ShippingAddressForm
from shipping import carrier

# Create your views here.
def _visible_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment.objects.select_related("auction__item", "buyer", "seller"), id=shipment_id)
    if request.user not in (shipment.buyer, shipment.seller) and not request.user.is_staff:
        return None
    return shipment


def _can_simulate(shipment):
    # Sellers ship for real; the demo shortcut only skips the carrier wait (or stands in for an unknown seller)
    if not settings.DEBUG:
        return False
    return shipment.status in carrier.TRANSIT_FLOW[:-1] or (shipment.status == "label_created" and not shipment.seller)


@login_required
def shipments(request):
    queryset = Shipment.objects.select_related("auction__item", "buyer", "seller").order_by("-created_at")
    for shipment in queryset.filter(Q(buyer=request.user) | Q(seller=request.user)):
        carrier.sync(shipment)
    context = {
        "purchases": queryset.filter(buyer=request.user),
        "sales": queryset.filter(seller=request.user),
    }
    return render(request, "shipping/shipments.html", context=context)


@login_required
def shipping_details(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id, buyer=request.user)
    if shipment.status != "awaiting_address":
        return redirect("track_shipment", shipment_id=shipment.id)
    if request.method == "POST":
        form = ShippingAddressForm(request.POST, instance=shipment)
        if form.is_valid():
            carrier.create_label(form.save(commit=False))
            return redirect("track_shipment", shipment_id=shipment.id)
    else:
        user = request.user
        form = ShippingAddressForm(instance=shipment, initial={
            "recipient_name": f"{user.first_name} {user.last_name}".strip() or user.username,
            "phone": user.phone or "",
            "address_line": user.address or "",
        })
    return render(request, "shipping/shipping_details.html", {"form": form, "shipment": shipment})


@login_required
def track_shipment(request, shipment_id):
    shipment = _visible_shipment(request, shipment_id)
    if shipment is None:
        return HttpResponseForbidden("You are not part of this shipment.")
    carrier.sync(shipment)
    steps = Shipment.STATUS_CHOICES[1:]
    context = {
        "shipment": shipment,
        "events": shipment.events.all(),
        "steps": steps,
        "current_step": shipment.status_index() - 1,
        "image": ItemImage.objects.filter(item=shipment.item).first(),
        "is_seller": request.user == shipment.seller,
        "can_simulate": _can_simulate(shipment),
    }
    return render(request, "shipping/track.html", context=context)


@login_required
@require_POST
def mark_shipped(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id, seller=request.user)
    if shipment.status == "label_created":
        carrier.mark_shipped(shipment)
    return redirect("track_shipment", shipment_id=shipment.id)


@login_required
@require_POST
def simulate_next(request, shipment_id):
    # Demo-only shortcut so you don't have to wait for the mock carrier.
    shipment = _visible_shipment(request, shipment_id)
    if shipment is None or not _can_simulate(shipment):
        return HttpResponseForbidden()
    carrier.advance(shipment)
    return redirect("track_shipment", shipment_id=shipment.id)
