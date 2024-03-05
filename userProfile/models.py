

import os
from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
def image_directory_path(instance,filename):
    ext=filename.split('.')[-1]
    filename=f'{uuid4()}.{ext}'
    user=str(instance.username)
    return os.path.join('media',user,'image',filename)

class Profile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,default='example@gmail.com',blank=False)
    first_name=models.CharField(max_length=50,default="")
    last_name=models.CharField(max_length=50,default="")
    username=models.CharField(max_length=50,unique=True,blank=False)
    image=models.ImageField(upload_to=image_directory_path,blank=True)
    created_at=models.DateField(auto_now_add=True)
    modified_at=models.DateField(auto_now=True)
    date_of_birth=models.DateField(null=True)
    password=models.CharField(max_length=250)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    objects = CustomUserManager()
    is_email_varified=models.BooleanField(default=False)
    vrf_code=models.CharField(max_length=32,default='')


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email




class FriendShip(models.Model):
    status_options=(
        ('P',"Pending"),
        ('A',"Accepted"),
        ('R','Rejected')
    )
    sender=models.ForeignKey(Profile,on_delete=models.CASCADE,null=False,blank=False,related_name='sent_friendships')
    reciever=models.ForeignKey(Profile,on_delete=models.CASCADE,null=False,blank=False,related_name='received_friendships')
    status=models.CharField(max_length=1,choices=status_options,default='P')
    created_at=models.DateField(auto_now_add=True)
    modified_at=models.DateField(auto_now=True)

    class Meta:
        unique_together=('sender','reciever')

    



    

