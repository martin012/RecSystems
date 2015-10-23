from django.db import models

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=50)
    
    def __str__(self):              # __unicode__ on Python 2
        return self.restaurant_name

class Food(models.Model):
    food_name = models.CharField(max_length=50)
    food = models.ForeignKey(Restaurant)

    def __str__(self):              # __unicode__ on Python 2
        return self.food_name