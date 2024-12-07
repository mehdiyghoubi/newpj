from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
# Create your views here.
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username= data['user_name'], email=data['email'], first_name=data['first_name'], last_name=data['last_name'] , password=data['password_2'])
            user.save()
            messages.success(request, 'Your account has been created!''success' , 'success')
            return redirect('home:home')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html' , {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = authenticate(request, username = User.objects.get(email=data['user']) , password = data['password'])
            except:
                user = authenticate(username=data['user'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in!' , 'info')
                return redirect('home:home')
            else:
                messages.error(request, 'Username or password is incorrect!' , 'danger')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html' , {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You are now logged out!' , 'warning')
    return redirect('home:home')

@login_required(login_url='accounts:login')
def user_profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request , 'accounts/profile.html' , {'profile':profile})

@login_required(login_url='accounts:login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST ,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST ,instance=request.user.profile)
        if user_form and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request , 'accounts/update.html' , {'user_form':user_form, 'profile_form':profile_form})

@login_required(login_url='accounts:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user , request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request , 'accounts/change.html' , {'form': form})