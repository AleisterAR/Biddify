from django import forms
from shipping.models import Shipment

INPUT_CLASSES = "field"


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ["recipient_name", "phone", "address_line", "city", "postal_code", "country", "method"]
        labels = {
            "recipient_name": "Full name",
            "address_line": "Street address",
            "method": "Delivery method",
        }
        widgets = {
            "method": forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.required = True
            if name != "method":
                field.widget.attrs["class"] = INPUT_CLASSES
