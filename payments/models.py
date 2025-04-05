from django.db import models
from participants.models import Participant
from bid.models import Auction

# Create your models here.
class Payment(models.Model):
    user_email = models.EmailField()
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_intent = models.CharField(max_length=255, unique=True)
    payment_status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_intent} - {self.amount}"