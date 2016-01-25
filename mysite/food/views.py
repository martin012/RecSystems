from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from django.conf import settings
import pygeoip
import socket 
import netifaces
from .models import Restaurant, Food, UserItem, User
from django.db.models import get_model
from math import sqrt
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
                list[i] = food = Food.objects.get(food_name = foods_recommend[i])
                i+=1
             
            # Algoritmus ak najde malo vhodnych vysledkov
            
            
            return render(request, 'food/templates/user_view.html', {'list': list, 'STATIC_PICS' : settings.STATIC_PICS })

        else:
            return render(request, 'food/templates/login.html')
    else:
        return render(request, 'food/templates/login.html')
 

def index(request):
    
    ####################################################
    
    geo = pygeoip.GeoIP(settings.GEOIP_CITY)
    
    # Kvoli sieti a nefunkcnosti v malych mestach kvoli testovaniu
    location = geo.record_by_addr('195.113.194.2' )
    
    country = location.get('country_name')
    city = location.get('city')
    return HttpResponse(country + ':  ' + city)

def basic(request):
    
    geo = pygeoip.GeoIP(settings.GEOIP_CITY)
    
    # Kvoli sieti a nefunkcnosti v malych mestach kvoli testovaniu
    IP_addr = '195.113.194.2' 
    
    records = geo.record_by_addr(IP_addr)
    
    country = records.get('country_name')
    city = records.get('city')
    
    compute_average_of_foods()

    list1 =  best_rated_foods()

    return render(request, 'food/templates/index.html', {'city' : city, 'list': list1, 'STATIC_PICS' : settings.STATIC_PICS })

# Method gets record about current location of user
# Record(type dict) contains information about country, city and others.  
def get_location():
    
    af_inet_adresses = []

    for interface in netifaces.interfaces():
        af_inet_adresses.append(netifaces.ifaddresses(interface).get(netifaces.AF_INET))
    
    user_ip_adress = af_inet_adresses[0][0].get('addr') 
    
    geo = pygeoip.GeoIP(settings.GEOIP_CITY)
    
    # Kvoli nefunkcnosti na niektorych sietiach a malych mestach
    IP_addr = '195.113.194.2' 
    
    records = geo.record_by_addr(IP_addr)
    
    return records


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

