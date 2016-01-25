from django.conf.urls import url

from . import views

urlpatterns = [
#    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
    url(r'^basic', views.basic, name='basic'),    
    url(r'^user_view', views.user_view, name='user_view'),
    url(r'^rate_food', views.rate_food, name='rate_food'),
    url(r'^similar_foods', views.similar_foods, name='similar_foods'),
    url(r'^show_all_foods', views.show_all_foods, name='show_all_foods'),
    url(r'^logout_view', views.logout_view), 
]

