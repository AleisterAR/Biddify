from django import forms
from django.core.exceptions import ValidationError
from bid.models import Auction, Bid
from django.utils import timezone
from django import forms
from django.utils.timezone import now

class AuctionForm(forms.ModelForm):
    starting_time = forms.DateTimeField(label="Starting Time", widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'field'}))
    ending_time = forms.DateTimeField(label="Ending Time", widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'field'}))

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
            self.add_error('starting_time', 'Choose when bidding opens.')
        
        if not ending_time:
            self.add_error('ending_time', 'Choose when bidding closes.')

        if starting_time and ending_time:
            if ending_time <= starting_time:
                self.add_error('ending_time', "Bidding has to close after it opens.")

        if starting_time and starting_time < now():
            self.add_error('starting_time', "Choose an opening time in the future.")

        return cleaned_data

class BidForm(forms.ModelForm):

    bid_amount = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'type': 'text', 'class': 'field ps-9 text-lg font-semibold figure', 'inputmode': 'numeric', 'autocomplete': 'off', 'aria-label': 'Your bid in euros', 'hx-swap-oob':'true'}))
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
                self.add_error('bid_amount',"Enter an amount above €0.")
            elif previous_bid := auction.bids.last():
                if bid_amount <= previous_bid.bid_amount:
                    self.add_error('bid_amount', f"Bid more than €{previous_bid.bid_amount}, the current highest bid.")
            elif starting_price := auction.item.starting_price:
                if bid_amount < starting_price:
                    self.add_error('bid_amount', f"The opening price is €{starting_price}. Bid at least that.")
        else:
            self.add_error('bid_amount',"Enter an amount to bid.")
        
        return cleaned_data