from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . import models
from django.contrib.auth.decorators import login_required
from users.models import UserProfile

# Create your views here.
@login_required(login_url='signin')
def index(request):
 return render(request,'index.html')

def signup(request):
 if request.method == 'POST':
  username = request.POST['username']
  email = request.POST['email']
  password = request.POST['password']
  password2 = request.POST['password2']

  if password == password2:
      if User.objects.filter(email = email).exists():
        messages.info(request, 'Email is already taken')
        return redirect('signup')
      elif User.objects.filter(username=username).exists():
        messages.info(request,'Username is already taken')
        return redirect('signup')
      else:
        user = User.objects.create_user(username=username, email=email,password=password)
        user.save()

        #log user in and direct to settings page
        user_login = authenticate(username=username,password=password)
        login(request,user_login)

        #create a profile object for new user 
        user_model = User.objects.get(username=username)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        new_profile.save()
        return redirect('settings')
  else:
     messages.info(request, 'Passwords dont match')
     return redirect('signup')
 else:
  return render(request, 'signup.html')
 

def signin(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user  = authenticate(username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('/')
    else: 
      messages.info(request, 'Credentials Invalid')
      return redirect('/signin')
  else:
    return render(request,"signin.html")
  
@login_required(login_url='signin')
def Logout(request):
  logout(request)
  return redirect('signin')
@login_required(login_url='signin')
def Settings(request):
  return render(request, 'settings.html')
