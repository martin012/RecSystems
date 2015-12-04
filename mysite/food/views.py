from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from django.conf import settings
import pygeoip
import socket 
import netifaces
from .models import Restaurant, Food

from django.contrib.auth import authenticate, login

def user_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    
    if user is not None:
        if user.is_active:
            login(request, user)
            return render(request, 'food/templates/user_view.html')

        else:
            return render(request, 'food/templates/login.html')
    else:
        return render(request, 'food/templates/login.html')
     
def index(request):
    
    ####################################################
    
    geo = pygeoip.GeoIP(settings.GEOIP_CITY)
    
    location = geo.record_by_addr(user_ip_adress)
    
    country = location.get('country_name')
    city = location.get('city')
    return HttpResponse(country + ':  ' + city)

def basic(request):
    
    geo = pygeoip.GeoIP(settings.GEOIP_CITY)
    
    IP_addr = '195.113.194.2' 
    
    records = geo.record_by_addr(IP_addr)
    
    country = records.get('country_name')
    city = records.get('city')

    restaurant = Restaurant.objects.get(pk=1)
    restaurant1 = Restaurant.objects.get(pk=2)
    restaurant2 = Restaurant.objects.get(pk=3)

    food = restaurant.food_set.all().get(pk=1)
    food1 = restaurant.food_set.all().get(pk=2)
    food2 = restaurant.food_set.all().get(pk=3)

    tags = food.tag_set.all()
    tags1 = food1.tag_set.all()
    tags2 = food2.tag_set.all()
    
 
    return render(request, 'food/templates/index.html', {'city' : city,'restaurant': restaurant, 'restaurant1': restaurant1, 'restaurant2': restaurant2,'food': food, 'food1': food1, 'food2': food2, 'tags': tags, 'tags1': tags1 , 'tags2': tags2, 'STATIC_PICS' : settings.STATIC_PICS })

# Method gets record about current location of user
# Record(type dict) contains information about country, city and others.  
def get_location():
    
    # 
    
    af_inet_adresses = []

    for interface in netifaces.interfaces():
        af_inet_adresses.append(netifaces.ifaddresses(interface).get(netifaces.AF_INET))
    
    user_ip_adress = af_inet_adresses[0][0].get('addr') 
    
    #
    
    geo = pygeoip.GeoIP(settings.GEOIP_CITY)
    
    IP_addr = '195.113.194.2' 
    
    records = geo.record_by_addr(IP_addr)
    
    return records