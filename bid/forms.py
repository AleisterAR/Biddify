from django import forms
from django.core.exceptions import ValidationError
from bid.models import Auction, Bid
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

class BidForm(forms.ModelForm):

    bid_amount = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'type': 'text', 'class': 'bg-gray-50 border border-gray-300 text-black text-sm font-sans font-medium focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5', 'hx-swap-oob':'true'}))
    class Meta:
        model = Bid
        fields = ['bid_amount', 'auction']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bid_amount'].required = False

    def clean(self):
        cleaned_data = super().clean()
        bid_amount = cleaned_data.get('bid_amount')
        if bid_amount is not None:
            auction = cleaned_data.get('auction')
            if bid_amount <= 0:
                self.add_error('bid_amount',"Your bid price must be more than zero!")
            elif previous_bid := auction.bids.last():
                if bid_amount <= previous_bid.bid_amount:
                    self.add_error('bid_amount', f"Your bid price must be more than the previous bid of € {previous_bid.bid_amount}!")
        else:
            self.add_error('bid_amount',"Bid price is required!")
        
        return cleaned_data