from django.db import models
from userProfile.models import *

from django.utils import timezone


# Create your models here.

def post_directory_path(instance,filename):
    ext=filename.split('.')[-1]
    filename=f'{uuid4()}.{ext}'
    user=str(instance.user.username)
    return os.path.join('media',user,'post',filename)
class Post(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    caption=models.TextField(blank=True)
    post=models.ImageField(upload_to=post_directory_path)
    likes=models.PositiveBigIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    modified_at = models.DateTimeField(auto_now=True,null=True)
    # dislikes=models.PositiveBigIntegerField(default=0)

    



