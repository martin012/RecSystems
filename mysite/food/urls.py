from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^basic', views.basic, name='basic'),  
    url(r'^user_view', views.user_view, name='user_view'),  
    
]

