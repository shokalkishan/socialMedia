from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import render,HttpResponse,redirect

def email_vrf_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Add your custom logic here
        user=request.user
        # is_email_varified
        if(user.is_email_varified==False):
            return redirect('userProfile:userlogin')
        return view_func(request, *args, **kwargs)
    
    return wrapper
