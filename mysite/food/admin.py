from django.contrib import admin
 
from .models import Food, Restaurant

class FoodInline(admin.TabularInline):
    model = Food
    extra = 3

class RestaurantAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['restaurant_name']}),
    ]
    inlines = [FoodInline]

admin.site.register(Restaurant, RestaurantAdmin) 