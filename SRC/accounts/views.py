from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from six import text_type

from books.models import Book, Category
from orders.models import Order

from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, AddressForm, \
    AddressUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Addresses, UserProfile
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin


class EmailToken(PasswordResetTokenGenerator):
    """برای ایجاد token هنگام ارسال ایمیل"""

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))


email_generator = EmailToken()


def user_register(request):
    """فانکشن برای ثبت نام کاربران میباشد"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email',)
            password = form.cleaned_data.get('password1',)
            first_name = form.cleaned_data.get('first_name',)
            last_name = form.cleaned_data.get('last_name',)
            address = form.cleaned_data.get('address',)
            user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name, password=password,)
            address = Addresses.objects.create(user=user, address=address, default=True)
            address.save()
            user.is_active = False
            user.save()
            """احراز هویت کاربر و ارسال ایمیل به کاربر"""
            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            url = reverse('accounts:active',kwargs={'uidb64': uidb64,'token': email_generator.make_token(user)})
            link = 'http://'+domain + url
            email = EmailMessage(
                'فعال شدن یوزر',
                link,
                'test<masoumeh.sedighii@gmail.com>',
                [email]
            )
            email.send(fail_silently=False)
            messages.warning(request, 'کاربر محترم جهت فعالسازی به ایمیل خود مراجعه فرمایید', 'warning')
            return redirect('book:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


class RegisterEmail(View):
    """بعد ار تایید فرم رجیستر توسط کاربر توکن و یوزر چک مبشود و میتواند لاکین کند"""
    def get(self, request, uidb64, token):
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if user and email_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('accounts:login')


def user_login(request):
    """مند برای لاکین کردن کاربر میباشد"""
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            print(user)
            print(cd)
            if user is not None:
                login(request, user)
                messages.success(request, 'شما با موفقیت از وارد سایت شدید', 'success')
                return redirect('book:home')
            else:
                messages.error(request, 'ایمیل با پسورد اشتباه است', 'danger')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    """ متذ برای خروج کاربر میباشد"""
    logout(request)
    messages.success(request, 'شما با موفقیت از سایت خارج شدید', 'success')
    return redirect('book:home')


def user_profile(request):
    """ساخت پروفایل کاربر"""
    profile = UserProfile.objects.get(user_id=request.user.id)
    return render(request, 'user_panel.html', {'profile': profile})


@login_required
def user_update(request):
    """اطلاعات کاربر و پروفایل آن را بروزرسانی میکند"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
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


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    """بروز رسانی آدرس توسط کاربر"""
    model = Addresses
    template_name = 'address_update.html'
    form_class = AddressUpdateForm
    success_url = reverse_lazy('accounts:address_profile')

    def post(self, request, *args, **kwargs):
        address = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            default = form.cleaned_data['default']
            """تغییر default سایر آدرس ها"""
            if default:
                other_instance = Addresses.objects.filter(user=request.user).exclude(id=address.id)
                print(other_instance)
                for addr in other_instance:
                    addr.default = False
                    addr.save()
            return super(AddressUpdateView, self).post(request, *args, **kwargs)


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    """حذف کردن آدرس توسط کاربر"""
    model = Addresses
    template_name = 'address_delete.html'
    fields = '__all__'
    success_url = reverse_lazy('accounts:address_profile')

    def delete(self, request, *args, **kwargs):
        """عدم امکان حذف حداقل یک آدرس"""
        object_addr = self.get_object()
        count_address = Addresses.objects.filter(user=request.user).count()
        if count_address > 1:
            object_addr.delete()
        else:
            messages.success(request, 'کاربر گرامی امکان حذف آدرس نمیباشد', 'success')
        return redirect('accounts:address_profile')


@login_required
def user_add_address(request):
    """اصافه کردن آدری در پروفایل توسط کاربر میباشذ"""
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


@login_required
def history_order(request):
    """تاریخچه سفارشات را در پروفایل کاربر نشان میدهد"""
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    context = {
               'orders': orders,
               }
    return render(request, 'history.html', context)


@login_required
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


class BookCreateView(LoginRequiredMixin, CreateView):
    """اضافه کردن کتاب توسط کارمند و ادمین"""
    permission_required = 'Book.add_book'
    model = Book
    template_name = 'book_new.html'
    fields = '__all__'
    success_url = reverse_lazy('accounts:profile')


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """اضافه کردن دسته بندی توسط کارمند و ادمین"""
    model = Category
    template_name = 'category_new.html'
    fields = '__all__'
    success_url = reverse_lazy('accounts:profile')


class BookDeleteView(LoginRequiredMixin, DeleteView):
    """حذف کردن کتاب توسط کارمند و ادمین"""
    model = Book
    template_name = 'book_delete.html'
    fields = '__all__'

    success_url = reverse_lazy('accounts:profile')


class BookListView(LoginRequiredMixin, ListView):
    """این متد لیست نمام کتاب ها را به مدیر و کارمند نشان میدهد"""
    model = Book
    template_name = 'staff_book_list.html'

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['staff_book_list'] = Book.objects.all()
        print(context)
        return context


class BookUpdateView(LoginRequiredMixin, UpdateView):
    """ویرایش کتاب توسط کارمند و ادمین"""
    model = Book
    template_name = 'staff_book_update.html'
    fields = '__all__'
    success_url = reverse_lazy('accounts:profile')



