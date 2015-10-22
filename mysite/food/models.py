from django.db import models

# Create your models here.

class UserLocation():
    text = models.CharField(max_length=200)
