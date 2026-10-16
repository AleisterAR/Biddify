from django.contrib import admin
from shipping.models import Shipment, ShipmentEvent
from shipping import carrier

# Register your models here.
class ShipmentEventInline(admin.TabularInline):
    model = ShipmentEvent
    extra = 0


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("auction", "buyer", "seller", "tracking_number", "status", "estimated_delivery")
    list_filter = ("status", "method")
    search_fields = ("tracking_number", "buyer__username", "seller__username")
    inlines = [ShipmentEventInline]
    actions = ["advance_status"]

    @admin.action(description="Advance to next shipping status (mock carrier)")
    def advance_status(self, request, queryset):
        for shipment in queryset:
            carrier.advance(shipment)


admin.site.register(ShipmentEvent)
