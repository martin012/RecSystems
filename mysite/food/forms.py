from django import forms
from .models import User, Food

class UserItemForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    food = forms.ModelChoiceField(queryset=Food.objects.all())
    rating = forms.DecimalField()
