from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegistrationForm, AddressForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Addresses


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
                messages.success(request, 'you logged in successfully', 'success')
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
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name, password=password,)
            address = Addresses.objects.create(user=user, address=address, default=True)
            address.save()
            user.save()
            messages.success(request, 'you registered successfully', 'success')
            return redirect('book:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_profile(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data.get('address')
            city = form.cleaned_data.get('city')
            phone = form.cleaned_data.get('phone')
            address = Addresses.objects.create(user=request.user, address=address, city=city, phone=phone)
            address.save()
            return redirect('accounts:profile')
    else:
        form = AddressForm()
    return render(request, 'user_panel.html', {'form': form})
