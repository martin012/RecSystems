from django.db import models

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=50)
    restaurant_description = models.CharField(max_length=50)
    restaurant_photo = models.ImageField(upload_to="images/restaurant/")
    restaurant_address = models.CharField(max_length=50, default = "")

    def __str__(self):              # __unicode__ on Python 2
        return self.restaurant_name
        
    def get_res_description(self):
        return self.restaurant_description

class Food(models.Model):
    food_name = models.CharField(max_length=50)
    food_photo = models.ImageField(upload_to="images/food/")
    food_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    food = models.ForeignKey(Restaurant)


    def __str__(self):              # __unicode__ on Python 2
        return self.food_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    tag = models.ForeignKey(Food)

    def __str__(self):              # __unicode__ on Python 2
        return self.tag_name