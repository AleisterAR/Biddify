from django.db import models
from participants.models import Participant
from django.utils import timezone

class Category(models.Model):
    category = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return f"{self.category}"
    
class Item(models.Model):
    CONDITION_TYPES = (
        ('mint', 'Mint'),
        ('near_mint', 'Near Mint'),
        ('excellent', 'Excellent'),
        ('very_good', 'Very Good'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    creator = models.CharField(max_length=255, null=True, blank=True, default="Annonymous")
    condition = models.CharField(max_length=255,choices=CONDITION_TYPES, null=True, blank=True)
    year = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey(Participant, on_delete=models.CASCADE)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    provenance = models.FileField(upload_to='provenance_documents/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.name}"
    
class ItemImage(models.Model):
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)