from django.urls import path 
from .views import *

app_name = 'emailVerification'
urlpatterns = [
    path('index/',index, name='index'), 
    path('sendCode/',send_verification_code, name='sendCode'), 
    path('index/verify/',verify,name='verify'),
    # Changed the URL pattern name to 'all_user'
]
