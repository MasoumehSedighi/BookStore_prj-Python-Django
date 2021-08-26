from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from books.models import Book, Category
from orders.models import Order
from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, AddressUpdateForm, \
    AddressForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Addresses, UserProfile
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


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
            user.is_active = False
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


class AddressUpdateView(UpdateView):
    model = Addresses
    template_name = 'address_update.html'
    fields = '__all__'
    success_url = reverse_lazy('accounts:profile')


class AddressDeleteView(DeleteView):
    """حذف کردن کتاب توسط کارمند و ادمین"""
    model = Addresses
    template_name = 'address_delete.html'
    fields = '__all__'
    success_url = reverse_lazy('accounts:address_profile')


def user_add_address(request):
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
    return render(request, 'address_new.html', {'form': form})


def history_order(request):
    """تاریخچه سفارشات را نشان میدهد"""
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    context = {
               'orders': orders,
               }
    return render(request, 'history.html', context)


def address_profile(request):
    """آدرس هر کاربر را در پروفایلش نشان میدهد"""
    current_user = request.user
    addresses = Addresses.objects.filter(user_id=current_user.id)
    context = {
               'addresses': addresses,
               }
    return render(request, 'address.html', context)


class ResetPassword(auth_views.PasswordResetView):
    """این قسمت مربوط به فراموشی پسورد میباشد"""
    template_name = 'reset.html'
    success_url = reverse_lazy('accounts:reset_done')
    email_template_name = 'link.html'


class DonePassword(auth_views.PasswordResetDoneView):
    """این قسمت مربوط به فراموشی پسورد میباشد"""
    template_name = 'done.html'


class ConfirmPassword(auth_views.PasswordResetConfirmView):
    """این قسمت مربوط به فراموشی پسورد میباشد"""
    template_name = 'confirm.html'
    success_url = reverse_lazy('accounts:complete')


class Complete(auth_views.PasswordResetCompleteView):
    """این قسمت مربوط به فراموشی پسورد میباشد"""
    template_name = 'complete.html'


class BookCreateView(CreateView):
    """اضافه کردن کتاب توسط کارمند و ادمین"""
    model = Book
    template_name = 'book_new.html'
    fields = '__all__'
    success_url = reverse_lazy('accounts:profile')


class CategoryCreateView(CreateView):
    """اضافه کردن دسته بندی توسط کارمند و ادمین"""
    model = Category
    template_name = 'category_new.html'
    fields = '__all__'
    success_url = reverse_lazy('accounts:profile')


class BookDeleteView(DeleteView):
    """حذف کردن کتاب توسط کارمند و ادمین"""
    model = Book
    template_name = 'book_delete.html'
    fields = '__all__'

    success_url = reverse_lazy('accounts:profile')


class BookListView(ListView):
    """این متد لیست نمام کتاب ها را به مدیر و کارمند نشان میدهد"""
    model = Book
    template_name = 'staff_book_list.html'

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['staff_book_list'] = Book.objects.all()
        print(context)
        return context


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'staff_book_update.html'
    fields = '__all__'

    success_url = reverse_lazy('accounts:profile')
