from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin 
from .models import Food, Restaurant, Tag,UserItem

class TagInline(NestedStackedInline):
    model = Tag
    extra = 3

class FoodInline(NestedStackedInline):
    model = Food
    extra = 3
    inlines = [TagInline]

class RestaurantAdmin(NestedModelAdmin):
    fieldsets = [
              (None, {'fields': ['restaurant_name','restaurant_description', 'restaurant_address', 'restaurant_photo']})
    ]
    inlines = [FoodInline]

class UserItemAdmin(NestedModelAdmin):
    fieldsets = [
              (None, {'fields': ['user', 'food', 'rating']})
    ]

admin.site.register(Restaurant, RestaurantAdmin) 
admin.site.register(UserItem, UserItemAdmin)
