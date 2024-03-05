from django.shortcuts import render,HttpResponse,redirect
from .forms import SignUpForm,LoginForm
from django.contrib.auth import authenticate, login,logout
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            # Extract cleaned data from the form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            date_of_birth = form.cleaned_data.get('date_of_birth')
            email = form.cleaned_data.get('email')
            
            
            # Create a new user profile
            user = Profile.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                email=email,
            
            )
            user.save()
            if 'image' in request.FILES:
                image = request.FILES['image']
                user.image = image
                user.save()
                print("Image uploaded successfully:", image)
            else:
                print("No image uploaded")


            
            return redirect('userProfile:userlogin')
    else:
        form = SignUpForm()
    
    # Render the signup form
    return render(request, 'userProfile/signup.html', {'form': form})

def userlogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:

                login(request, user)
                if user.is_email_varified == False:
                    return redirect('emailVerification:index')

                return redirect('home:home')
            else:
                error_message = "Invalid username or password."
                return render(request, 'userProfile/login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    return render(request, 'userProfile/login.html', {'form': form})

@login_required
def userlogout(request):
    logout(request)

    return redirect('userProfile:userlogin')  
