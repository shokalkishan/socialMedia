from django.shortcuts import render,HttpResponse,redirect
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from django.urls import reverse
from userProfile.models import Profile

def index(request):
    return render(request,'emailVerification/index.html',{'user':request.user})

def generate_verification_code(user):
    code=get_random_string(length=8)
    user.vrf_code=code
    user.save()

    return 
def send_verification_code(request):
    user=request.user

    new_email=request.POST.get('email')
    if(new_email):
        user.email=new_email
        user.save()
    generate_verification_code(user)
    code=user.vrf_code
    url=f'http://10.5.49.90:8000'+reverse('emailVerification:index')+f'verify/{user.username}/{code}/'
    

    subject='Verify Your Account'
    message=f'Verification Code is : {code}'

    mail_to=[user.email]
    mail_from=settings.EMAIL_HOST_USER
    # mail_from='shokal812@gmail.com'

    send_mail(subject,message,mail_from,mail_to,fail_silently=False)
    return render(request,'emailVerification/verify.html',{'user':request.user})

def verify(request):
    # user=Profile.objects.filter(username=user)[0]
    print('verify')
    user=request.user
    print(user)
    code=request.POST.get('code')
    print(code)

    # code=request.GET.get('code')
    if(code==user.vrf_code):
        user.is_email_varified=True
        user.save()
        return redirect('home:home')
    return redirect('userProfile:userlogin')