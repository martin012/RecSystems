from django.contrib import admin
 
from .models import Food, Restaurant

class FoodInline(admin.TabularInline):
    model = Food
    extra = 10

class RestaurantAdmin(admin.ModelAdmin):
    fieldsets = [
              (None, {'fields': ['restaurant_name','restaurant_description', 'restaurant_photo']})
    ]
    inlines = [FoodInline]

admin.site.register(Restaurant, RestaurantAdmin) 