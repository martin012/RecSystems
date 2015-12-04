from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin 
from .models import Food, Restaurant, Tag

class TagInline(NestedStackedInline):
    model = Tag
    extra = 3

class FoodInline(NestedStackedInline):
    model = Food
    extra = 3
    inlines = [TagInline]

class RestaurantAdmin(NestedModelAdmin):
    fieldsets = [
              (None, {'fields': ['restaurant_name','restaurant_description', 'restaurant_photo']})
    ]
    inlines = [FoodInline]

admin.site.register(Restaurant, RestaurantAdmin) 