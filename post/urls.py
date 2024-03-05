from django.urls import path 
from .views import *

app_name = 'post'
urlpatterns = [
    path('create-post/', create_post, name='create_post'), 
    path('like-post/',like_post,name='like_post'),
    path('delete-post/',delete_post,name='delete_post'),

    # Changed the URL pattern name to 'all_user'
]
