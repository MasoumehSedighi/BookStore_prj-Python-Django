from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            print(user)
            print(cd)
            if user is not None:
                login(request, user)
                # messages.success(request, 'you logged in successfully', 'success')
                return redirect('book:home')
            else:
                messages.error(request, 'ایمیل با پسورد اشتباه است', 'danger')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'you logged out successfully', 'success')
    return redirect('book:home')


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['email'], cd['full_name'], cd['password'])
            user.save()
            messages.success(request, 'you registered successfully', 'success')
            return redirect('shop:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})