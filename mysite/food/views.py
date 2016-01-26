from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from django.conf import settings
import pygeoip
import socket 
import netifaces
import math
from math import sqrt
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
        
def similar_foods(request):
    if request.user.is_authenticated():
        if request.POST:   
            food = request.POST['in-food']
            food1 = Food.objects.get(id = food)
            list_of_foods = sim_item_tags(food1)
            return render(request, 'food/templates/simfoodslog.html', {'food': food1, 'list': list_of_foods, 'STATIC_PICS' : settings.STATIC_PICS })          
    else: 
        if request.POST:
            food = request.POST['in-food']
            food1 = Food.objects.get(id = food)
            list_of_foods = sim_item_tags(food1)
            return render(request, 'food/templates/simfoods.html', {'food': food1, 'list': list_of_foods, 'STATIC_PICS' : settings.STATIC_PICS })          

def user_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
   
    if user is not None:
        if user.is_active:
            login(request, user)

            dataset = get_dataset()
            foods_recommend = user_recommendations(dataset, user.username)
            
            food_count = len(foods_recommend)
            
            list = []
            
            i = 0
            for f in foods_recommend:
                list.append(Food.objects.get(food_name = foods_recommend[i]))
                i += 1
                
            # Algoritmus ak najde malo vhodnych vysledkov
            
            
            return render(request, 'food/templates/user_view.html', {'list': list[0:4], 'STATIC_PICS' : settings.STATIC_PICS })

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
    #food1_sim_item = sim_item_tags(best_rated_food[0])
    #food2_sim_item = sim_item_tags(best_rated_food[1])
    #food3_sim_item = sim_item_tags(best_rated_food[2]) 
    #food4_sim_item = sim_item_tags(best_rated_food[3])
    #similar_zip_foods = zip(best_rated_food1, best_rated_food2, best_rated_food3, best_rated_food4)
    #finalzip = zip(best_rated_foods, similar_zip_foods)
    
    return render(request, 'food/templates/index.html', {'city' : city, 'list': best_rated_food,'STATIC_PICS' : settings.STATIC_PICS })

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

def user_recommendations(dataset, person):

	# Gets recommendations for a person by using a weighted average of every other user's rankings
	totals = {}
	simSums = {}
	rankings_list =[]
	for other in dataset:
		# don't compare me to myself
		if other == person:
			continue
		sim = pearson_correlation(dataset, person, other)
		#print ">>>>>>>",sim

		# ignore scores of zero or lower
		if sim <=0: 
			continue
		for item in dataset[other]:

			# only score movies i haven't seen yet
			if item not in dataset[person] or dataset[person][item] == 0:

			# Similrity * score
				totals.setdefault(item,0)
				totals[item] += dataset[other][item]* sim
				# sum of similarities
				simSums.setdefault(item,0)
				simSums[item]+= sim

		# Create the normalized list

	rankings = [(total/simSums[item],item) for item,total in totals.items()]
	rankings.sort()
	rankings.reverse()
	# returns the recommended items
	recommendataions_list = [recommend_item for score,recommend_item in rankings]
	return recommendataions_list
 
def pearson_correlation(dataset, person1,person2):

	# To get both rated items
	both_rated = {}
	for item in dataset[person1]:
		if item in dataset[person2]:
			both_rated[item] = 1

	number_of_ratings = len(both_rated)		
	
	# Checking for number of ratings in common
	if number_of_ratings == 0:
		return 0

	# Add up all the preferences of each user
	person1_preferences_sum = sum([dataset[person1][item] for item in both_rated])
	person2_preferences_sum = sum([dataset[person2][item] for item in both_rated])

	# Sum up the squares of preferences of each user
	person1_square_preferences_sum = sum([pow(dataset[person1][item],2) for item in both_rated])
	person2_square_preferences_sum = sum([pow(dataset[person2][item],2) for item in both_rated])

	# Sum up the product value of both preferences for each item
	product_sum_of_both_users = sum([dataset[person1][item] * dataset[person2][item] for item in both_rated])

	# Calculate the pearson score
	numerator_value = product_sum_of_both_users - (person1_preferences_sum*person2_preferences_sum/number_of_ratings)
	denominator_value = sqrt((person1_square_preferences_sum - pow(person1_preferences_sum,2)/number_of_ratings) * (person2_square_preferences_sum -pow(person2_preferences_sum,2)/number_of_ratings))
	if denominator_value == 0:
		return 0
	else:
		r = numerator_value/denominator_value
		return r 

def get_dataset():
    
    users = User.objects.all()

    user_foods_dict = {} 

    for usr in users:

        user_foods = UserItem.objects.filter(user = usr)
        food_rating_dict = {}
        
        for usr_foods in user_foods: 
            food_name = usr_foods.food.food_name
            rating = usr_foods.rating
            
            food_rating_dict.update({food_name : rating})
    
        user_foods_dict.update({usr.username : food_rating_dict})
        
    return user_foods_dict
