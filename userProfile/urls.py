
from django.urls import path 
from .views import *
app_name='userProfile'
urlpatterns = [
    path('signup/',signup,name='signup'),
    path('login/',userlogin,name='userlogin'),
    path('logout/',userlogout,name='logout'),
    
]