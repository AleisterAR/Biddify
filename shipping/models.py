from django.db import models
from django.utils import timezone
from participants.models import Participant
from bid.models import Auction
from payments.models import Payment
import pycountry

# Create your models here.
class Shipment(models.Model):
    STATUS_CHOICES = (
        ('awaiting_address', 'Awaiting address'),
        ('label_created', 'Label created'),
        ('shipped', 'Shipped'),
        ('in_transit', 'In transit'),
        ('out_for_delivery', 'Out for delivery'),
        ('delivered', 'Delivered'),
    )
    METHOD_CHOICES = (
        ('standard', 'Standard (3-5 business days)'),
        ('express', 'Express (1-2 business days)'),
    )
    COUNTRY_CHOICES = sorted([(country.name, country.name) for country in pycountry.countries], key=lambda x: x[1])

    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name="shipment")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="shipments")
    buyer = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="purchases")
    seller = models.ForeignKey(Participant, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales")

    recipient_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address_line = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=255, choices=COUNTRY_CHOICES, blank=True)

    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='standard')
    carrier = models.CharField(max_length=100, default='Biddify Express')
    tracking_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='awaiting_address')
    estimated_delivery = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Shipment for {self.auction.item.name} ({self.get_status_display()})"

    @property
    def item(self):
        return self.auction.item

    def status_index(self):
        return [key for key, _ in self.STATUS_CHOICES].index(self.status)

    def is_delivered(self):
        return self.status == 'delivered'


class ShipmentEvent(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="events")
    status = models.CharField(max_length=30, choices=Shipment.STATUS_CHOICES)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f"{self.shipment.tracking_number} - {self.get_status_display()}"
