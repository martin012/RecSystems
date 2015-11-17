from django.db import models

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=50)
    restaurant_description = models.CharField(max_length=50)
    restaurant_photo = models.ImageField(upload_to="images/restaurant/")

    def __str__(self):              # __unicode__ on Python 2
        return self.restaurant_name
        
    def get_res_description(self):
        return self.restaurant_description

class Food(models.Model):
    food_name = models.CharField(max_length=50)
    food_photo = models.ImageField(upload_to="images/food/")
    food = models.ForeignKey(Restaurant)

    def __str__(self):              # __unicode__ on Python 2
        return self.food_name