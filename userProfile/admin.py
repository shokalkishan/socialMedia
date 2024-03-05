from django.contrib import admin
from .models import Profile, FriendShip

admin.site.register(Profile)
# admin.site.register(FriendShip)

class FriendShipAdmin(admin.ModelAdmin):
    list_display = ['sender', 'reciever', 'status', 'created_at']  # Define which fields to display in the admin list view

admin.site.register(FriendShip, FriendShipAdmin)
