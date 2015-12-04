from django.db import models

class Restaurant(models.Model):
    restaurant_name = models.CharField(blank = False, max_length = 50)
    restaurant_description = models.CharField(max_length = 50)
    restaurant_photo = models.ImageField(upload_to="images/restaurant/")

    def __str__(self):              # __unicode__ on Python 2
        return self.restaurant_name
        
    def get_res_description(self):
        return self.restaurant_description

class Food(models.Model):
    food_name = models.CharField(blank = False, max_length = 50)
    food_photo = models.ImageField(upload_to="images/food/")
    food_rating = models.DecimalField(max_digits = 2, decimal_places = 1, default = 0.0)
    food_restaurant = models.ForeignKey(Restaurant, null = False, on_delete = models.CASCADE)

    def __str__(self):              # __unicode__ on Python 2
        return self.food_name

class User(models.Model):
    name = models.CharField(blank=False, max_length=50)
     
class ItemUser(models.Model):
    user = models.ManyToManyField(User, null = False)
    food = models.ManyToManyField(Food, null = False)
    score = models.DecimalField(max_digits = 2, decimal_places =1, default = 0.0)
    