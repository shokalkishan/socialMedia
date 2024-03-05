from django.db import models
from post.models import *

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    parent_comment=models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,related_name='replies')
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

