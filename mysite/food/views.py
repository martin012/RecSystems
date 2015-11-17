from django.template.context_processors import csrf
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.conf import settings
import pygeoip
import socket 
import netifaces

def basic(request):
    
    location = get_location()
    
    country = location.get('country_name')
    city = location.get('city')
        
    return render(request, 'food/templates/index.html', {'country' : country, 'city' : city, 'STATIC_PICS' : settings.STATIC_PICS })


def user_view(request):
#    c = {}
#    c.update(csrf(request))
#    
#    #email = request.POST.get('cur_email')
#    email = request.POST
#    
##    
#    c = {}
#    c.update(csrf(request))
    
    email = request.GET
    #email = request.POST.get('cur_email')
    
    return render_to_response("food/templates/index2.html", {'email' : email})
    
    
    
    #return render(request, "food/templates/index2.html", {'email' : email})

# Method gets record about current location of user
# Record(type dict) contains information about country, city and others.  
def get_location():
    
    geo = pygeoip.GeoIP(settings.GEOIP_CITY)
    
    af_inet_adresses = []

    for interface in netifaces.interfaces():
        af_inet_adresses.append(netifaces.ifaddresses(interface).get(netifaces.AF_INET))
    
    user_ip_adress = '195.113.194.2' #af_inet_adresses[0][0].get('addr') 
    
    record = geo.record_by_addr(user_ip_adress)
    
    return record