from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from django.conf import settings
import pygeoip
import socket 
import netifaces
from .models import Restaurant, Food, UserItem, User
from django.db.models import get_model


from django.contrib.auth import authenticate, login, logout

def logout_view(request):
    logout(request)
    return render(request, 'food/templates/logout.html')

def rate_food(request):
    if request.user.is_authenticated():
        if request.POST:            
            #username = request.POST['in-username']
            #password = request.POST['in-password']
            username = request.user.username
            food = request.POST['in-food']
            rating = request.POST['in-rating'] 

            user = User.objects.get(username = username)
            food = Food.objects.get(id = food)
               
            try:
                useritemexist = UserItem.objects.get(user=user, food=food)
                return render(request, 'food/templates/ratingno.html', {'food': food})
            except UserItem.DoesNotExist:
                useritem = UserItem(user=user, food=food, rating=rating)
                useritem.save()
                return render(request, 'food/templates/rating.html', {'food': food, 'rating': rating })
    
        

def user_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
   
    if user is not None:
        if user.is_active:
            login(request, user)
            
            food = Food.objects.get(pk=1)
            food1 = Food.objects.get(pk=2)
            food2 = Food.objects.get(pk=14)
            food3 = Food.objects.get(pk=9)

            list = [food, food1, food2, food3]    

            return render(request, 'food/templates/user_view.html', {'list': list, 'STATIC_PICS' : settings.STATIC_PICS })

        else:
            return render(request, 'food/templates/login.html')
    else:
        return render(request, 'food/templates/login.html')
 
    
    
def index(request):
    
    ####################################################
    
    geo = pygeoip.GeoIP(settings.GEOIP_CITY)
    
    location = geo.record_by_addr('195.113.194.2' )
    
    country = location.get('country_name')
    city = location.get('city')
    return HttpResponse(country + ':  ' + city)

def basic(request):
    
    geo = pygeoip.GeoIP(settings.GEOIP_CITY)
    
    IP_addr = '195.113.194.2' 
    
    records = geo.record_by_addr(IP_addr)
    
    country = records.get('country_name')
    city = records.get('city')

    food = Food.objects.get(pk=1)
    food1 = Food.objects.get(pk=2)
    food2 = Food.objects.get(pk=14)
    food3 = Food.objects.get(pk=9)

    list = [food, food1, food2, food3]

    return render(request, 'food/templates/index.html', {'city' : city, 'list': list, 'STATIC_PICS' : settings.STATIC_PICS })

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