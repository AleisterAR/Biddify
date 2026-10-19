from django import forms
from participants.models import Participant


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["first_name", "last_name", "email", "phone", "address"]
        labels = {
            "first_name": "First name",
            "last_name": "Last name",
            "email": "Email",
            "phone": "Phone",
            "address": "Delivery address",
        }
        widgets = {
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel", "inputmode": "tel"}),
            "address": forms.Textarea(attrs={"rows": 4, "autocomplete": "street-address"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["autocomplete"] = "given-name"
        self.fields["last_name"].widget.attrs["autocomplete"] = "family-name"
        self.fields["email"].required = True
        for field in self.fields.values():
            field.widget.attrs["class"] = "field"

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if Participant.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Another account already uses this email.")
        return email
