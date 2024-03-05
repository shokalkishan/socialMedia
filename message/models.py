from django.db import models
from userProfile.models import Profile



class Message(models.Model):
    sender = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE,related_name='sent_message')
    receiver = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE,related_name='received_message')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



