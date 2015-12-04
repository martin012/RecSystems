from django.conf.urls import url

from . import views

urlpatterns = [
#    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
    url(r'^basic', views.basic, name='basic'),    
    url(r'^user_view', views.user_view), 
    url(r'^logout_view', views.logout_view), 
    
]

