from django.urls import path 
from .views import *

app_name = 'msg'
urlpatterns = [
    path('all/', all_user, name='all_user'), 
    path('<str:friend>/friend-list/',add_friend,name='add_friend'),
    path('friends/',friends,name='friends'),
    path('update/<str:sender>/<str:status>/',update_status,name='update_status'),
    path('chat/<str:reciever>/',chat,name='chat'),
    path('save-chat/',save_chat,name='save_chat')
    
    # Changed the URL pattern name to 'all_user'
]
