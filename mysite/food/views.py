from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from django.conf import settings
import pygeoip
import socket 
import netifaces
import math
from .models import Restaurant, Food, UserItem, User, Tag
from django.db.models import get_model



from django.contrib.auth import authenticate, login, logout

def compute_average_of_foods():
    for food in Food.objects.all():
        sum = 0.0;
        count = 0
        useritems = UserItem.objects.filter(food = food)
        
        # compute average for specified item
        for item1 in useritems:
            sum = sum + item1.rating
            count = count + 1
        try:
            food.food_rating = round(float(sum / float(count)), 1)
            food.save()
        except:
            # if it is exception division by zero, just skip it
            pass
    

def best_rated_foods():
    foods = Food.objects.order_by('-food_rating')
    return foods[0:4]



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
                UserItem.objects.get(user=user, food=food)
                return render(request, 'food/templates/ratingno.html', {'food': food})
            except UserItem.DoesNotExist:
                useritem = UserItem(user=user, food=food, rating=rating)
                useritem.save()
                return render(request, 'food/templates/rating.html', {'food': food, 'rating': rating })
            
def show_all_foods(request):
    if request.user.is_authenticated():
        if request.POST:   
            list_of_foods = Food.objects.all()
            return render(request, 'food/templates/allfoods.html', {'list': list_of_foods, 'STATIC_PICS' : settings.STATIC_PICS })
        

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

            list = [food, food1, food2]   
            

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
    
    compute_average_of_foods()
    
    #food = Food.objects.get(pk=1)
    #food1 = Food.objects.get(pk=2)
    #food2 = Food.objects.get(pk=14)
    #food3 = Food.objects.get(pk=9)
    #sim_item_tags(food)
    
    #list = [food, food1, food2, food3]
    
    best_rated_food =  best_rated_foods()
    food1_sim_item = sim_item_tags(best_rated_food[0])
    food2_sim_item = sim_item_tags(best_rated_food[1])
    food3_sim_item = sim_item_tags(best_rated_food[2]) 
    food4_sim_item = sim_item_tags(best_rated_food[3]) 
    
    #similar_zip_foods = zip(zip(food1_sim_item,best_rated_food[0]), zip(food2_sim_item,best_rated_food[1]), zip(food3_sim_item,best_rated_food[2]), zip(food4_sim_item, best_rated_food[3]))
    #finalzip = zip(best_rated_foods, similar_zip_foods)
    
    return render(request, 'food/templates/index.html', {'city' : city, 'list': best_rated_food,'food1_sim_item': food1_sim_item, 'food2_sim_item': food2_sim_item, 'food3_sim_item': food3_sim_item, 'food4_sim_item': food4_sim_item,'STATIC_PICS' : settings.STATIC_PICS })

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

def cos_sim_recipes_tags(food1, food2):
    all_tags = Tag.objects.values('tag_name').distinct().order_by()
    if food1.id == food2.id: return 0.0
    if len(Tag.objects.filter(food = food1)) == 0 or len(Tag.objects.filter(food = food2)) == 0: return 0.0

    vector1 = []
    vector2 = []

    for tag in all_tags:
      
        if tag in Tag.objects.filter(food = food1).values('tag_name'):
            vector1.append(1.0)
        else:
            vector1.append(0.0)
        if tag in Tag.objects.filter(food = food2).values('tag_name'):
            vector2.append(1.0)
        else:
            vector2.append(0.0)
    
    numerator, pow1, pow2 = 0.0, 0.0, 0.0

    for i in range(0, len(all_tags)):
        numerator = numerator + (vector1[i] * vector2[i])
        pow1 = pow1 + (vector1[i] * vector1[i])
        pow2 = pow2 + (vector2[i] * vector2[i])

    denumerator = math.sqrt(pow1) * math.sqrt(pow2)
   
    if denumerator == 0.0:
        return 0.0
    else: 
        return numerator / denumerator

class SimilarObject(object):
    def __init__(self, food_id, similarity_value):
        self.food_id = food_id
        self.similarity_value = similarity_value    

def get_similarity_key(custom):
    return custom.similarity_value

def get_id_key(custom):
    return custom.food_id
    
def sim_item_tags(food1):
    
    sim_array = []
    for food2 in Food.objects.all():
        if food2.id == food1.id: continue
        sim_array.append(SimilarObject(food2.id, cos_sim_recipes_tags(food1, food2)))
    newlist = sorted(sim_array, key=get_similarity_key, reverse=True)
    
    simitem = []
    for item in newlist[0:3]:
        simitem.append(Food.objects.get(id = get_id_key(item)))
    return simitem
    
def similar_items(items):
  
    sim_items = []
    for item1 in items:
        sim_items.append(sim_item_tags(item1))
    return sim_items    