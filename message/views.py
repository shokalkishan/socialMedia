from django.shortcuts import render,redirect,HttpResponse
from django.db.models import Q
from userProfile.models import Profile,FriendShip
from .models import Message
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from emailVerification.decorators import email_vrf_required

@login_required
@email_vrf_required
def all_user(request):

    user=request.user
    users=Profile.objects.exclude(username = user.username)
    users_details=[]
    for ele in users:
        status=FriendShip.objects.filter(Q(Q(sender=user) & Q(reciever=ele))| Q(Q(sender=ele) & Q(reciever=user)))
        relation=[ele,'N']
        if(len(status)==1):
            relation[1]=status[0].status
        users_details.append(relation)

    paginator = Paginator(users_details, 5)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={
        'user':user,
        'users':page_obj
    }
    return render(request,"message/all_user.html",context)
@login_required
@email_vrf_required
def friends(request):
    user=request.user
    pending_req=FriendShip.objects.filter(reciever=user,status='P')
    friend=FriendShip.objects.filter(Q(Q(sender=user) | Q(reciever=user)) & Q(status='A'))
    friends=[]
    for ele in friend:
        if ele.sender.username==user.username:
            friends.append(ele.reciever)
        else :
            friends.append(ele.sender)

    paginator = Paginator(friends, 5)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj1 = paginator.get_page(page_number)
    paginator = Paginator(pending_req, 5)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj2 = paginator.get_page(page_number)
    
    context={
        'friend_req':page_obj2,
        'friends':page_obj1,
        'user':user,
    }
    return render(request,'message/friends.html',context)
@login_required
@email_vrf_required
def add_friend(request,friend):


    friend=Profile.objects.filter(username=friend)
    if(len(friend)==0):
        return HttpResponse('friend len is zero (add_friend)')
    friend=friend[0]
    user=request.user
    friendship=FriendShip(sender=user,reciever=friend)
    friendship.save()


    return redirect('msg:all_user')



@login_required
@email_vrf_required
def update_status(request,sender,status):
    reciver=request.user
    tmp=sender
    sender=Profile.objects.filter(email=sender)[0]
    friend_ship=FriendShip.objects.filter(sender=sender,reciever=reciver)[0]
    friend_ship.status=status
    friend_ship.save()
    return redirect('msg:friends')

@login_required
@email_vrf_required
def chat(request,reciever):
    user=request.user
    reciever=Profile.objects.filter(username=reciever)[0]
    messages=Message.objects.filter(Q(Q(sender=user) & Q(receiver=reciever)) 
                                    |Q(Q(sender=reciever) & Q(receiver=user)) ).order_by('-created_at')[:15]
    messages=messages[::-1]
    context={
        'user':user,
        'reciever':reciever,
        'messages':messages
    }

    return render(request,'message/chat.html',context)

@login_required
@email_vrf_required
def save_chat(request):
    sender=request.user
    reciever=Profile.objects.filter(username=request.POST.get('reciever'))[0]
    msg=request.POST.get('message')
    if(len(msg)>0):
        obj=Message.objects.create(sender=sender,receiver=reciever,message=msg)
        obj.save()

    return redirect('msg:chat',reciever=reciever.username)


