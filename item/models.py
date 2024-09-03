from django.db import models
from participants.models import Participant
from django.utils import timezone

class Category(models.Model):
    category = models.CharField(max_length=255)
    
# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    year = models.CharField(max_length=255)
    owner = models.ForeignKey(Participant, on_delete=models.CASCADE)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.name}"
    
class ItemImage(models.Model):
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)