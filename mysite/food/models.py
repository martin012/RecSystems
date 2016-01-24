from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=50)
    restaurant_description = models.CharField(max_length=50)
    restaurant_photo = models.ImageField(upload_to="images/restaurant/")
    restaurant_address = models.CharField(max_length=100, default = "")

    def __str__(self):              # __unicode__ on Python 2
        return self.restaurant_name
        
    def get_res_description(self):
        return self.restaurant_description

class Food(models.Model):
    food_name = models.CharField(max_length=50)
    food_photo = models.ImageField(upload_to="images/food/")
    food_rating = models.FloatField(default=0)
    restaurant = models.ForeignKey(Restaurant)

    def __str__(self):              # __unicode__ on Python 2
        return self.food_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    food = models.ForeignKey(Food)

    def __str__(self):              # __unicode__ on Python 2
        return self.tag_name

class UserItem(models.Model):
    user = models.ForeignKey(User) 
    food = models.ForeignKey(Food)
    rating = models.FloatField(default=0)

    def __str__(self):
        return "User: {0}, Food: {1}, Rating: {2}".format(self.user.username, self.food.food_name, self.rating)

