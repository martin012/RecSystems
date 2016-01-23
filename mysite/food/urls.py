from django.conf.urls import url

from . import views

urlpatterns = [
#    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
    url(r'^basic', views.basic, name='basic'),    
    url(r'^user_view', views.user_view, name='user_view'),
    url(r'^rate_food', views.rate_food, name='rate_food'),
    url(r'^logout_view', views.logout_view), 
]

