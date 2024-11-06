from django import forms
from django.core.exceptions import ValidationError
from bid.models import Auction
from django.utils import timezone

from django import forms
from django.utils.timezone import now

class AuctionForm(forms.ModelForm):
    starting_time = forms.DateTimeField(label="Starting Time", widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'}))
    ending_time = forms.DateTimeField(label="Ending Time", widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'}))

    class Meta:
        model = Auction 
        fields = ['starting_time', 'ending_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['starting_time'].required = False
        self.fields['ending_time'].required = False

    def clean(self):
        cleaned_data = super().clean()
        starting_time = cleaned_data.get("starting_time")
        ending_time = cleaned_data.get("ending_time")

        if not starting_time:
            self.add_error('starting_time', 'Starting time is required!')
        
        if not ending_time:
            self.add_error('ending_time', 'Ending time is required!')

        if starting_time and ending_time:
            if ending_time <= starting_time:
                self.add_error('ending_time', "Ending time must be later than starting time.")

        if starting_time and starting_time < now():
            self.add_error('starting_time', "Starting time must be in the future.")

        return cleaned_data

