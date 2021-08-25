from django.shortcuts import render, redirect
from orders.models import OrderItem
from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Addresses, UserProfile


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
    profile = UserProfile.objects.get(user_id=request.user.id)
    return render(request, 'user_panel.html', {'profile': profile})


def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'بروز رسانی با موفقیت انجام شد', 'success')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'update.html', context)


def history(request):
    data = OrderItem.objects.filter(user_id=request.user.id)
    return render(request, 'history.html',data)


