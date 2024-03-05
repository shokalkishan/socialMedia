from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from post.models import Post
from userProfile.models import Profile , FriendShip
from django.db.models import Q
from django.core.paginator import Paginator
from emailVerification.decorators import email_vrf_required

# Create your views here.
@email_vrf_required
def find_posts(request):
    user=request.user
    posts=Post.objects.filter(
        Q(user=user) | 
        Q(user__in = [obj.reciever for obj in FriendShip.objects.filter(sender=user,status='A')]) |
        Q(user__in = [obj.sender for obj in FriendShip.objects.filter(reciever=user,status='A')]) 
    )

    return posts


@login_required
@email_vrf_required
def home(request):
    user=request.user
    posts=find_posts(request)


    paginator = Paginator(posts, 2)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # return render(request, 'my_template.html', {'page_obj': page_obj})
    context={
        'user':user,
        'posts':page_obj
    }

    return render(request,'home/home.html',context)

