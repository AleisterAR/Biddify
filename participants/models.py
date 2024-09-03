from django.db import models
from django.contrib.auth.models import AbstractUser

class Participant(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('participant', 'Participant'),
    )
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True, max_length=255)
    user_type = models.CharField(max_length=255, choices=USER_TYPE_CHOICES, default='participant')

    def __str__(self):
        return self.username