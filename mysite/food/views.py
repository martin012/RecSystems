from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from django.conf import settings
import pygeoip
import socket 
import netifaces
from .models import Restaurant, Food


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
    food1 = restaurant1.food_set.all().get(pk=4)
    food2 = restaurant2.food_set.all().get(pk=8)
 
    return render(request, 'food/templates/index.html', {'city' : city,'restaurant': restaurant, 'restaurant1': restaurant1, 'restaurant2': restaurant2,'food': food, 'food1': food1, 'food2': food2 ,'STATIC_PICS' : settings.STATIC_PICS })

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