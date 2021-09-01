from idlelib import history

from accounts.forms import UserRegistrationForm, UserLoginForm, AddressForm
from accounts.models import User
from accounts.models import UserProfile
from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from accounts.views import user_register, BookDeleteView, BookListView, user_profile, AddressUpdateView, \
    user_add_address, history_order, CategoryCreateView


class TestUrls(SimpleTestCase):
    def test_register(self):
        url = reverse('accounts:register')
        self.assertEqual(resolve(url).func, user_register)
        print(url)
        print(resolve(url))

    def test_book_list(self):
        url = reverse('accounts:staff_book_list')
        self.assertEqual(resolve(url).func.view_class, BookListView)
        print(url)
        print(resolve(url))

    def test_book_delete(self):
        url = reverse('accounts:book_delete', args=['5', ])
        self.assertEqual(resolve(url).func.view_class, BookDeleteView)
        print(url)
        print(resolve(url))

    def test_user_profile(self):
        url = reverse('accounts:profile')
        self.assertEqual(resolve(url).func, user_profile)
        print(url)
        print(resolve(url))

    def test_update_address(self):
        url = reverse('accounts:update_address', args=['5', ])
        self.assertEqual(resolve(url).func.view_class, AddressUpdateView)
        print(url)
        print(resolve(url))

    def test_address_new(self):
        url = reverse('accounts:address_new')
        self.assertEqual(resolve(url).func, user_add_address)
        print(url)
        print(resolve(url))

    def test_history(self):
        url = reverse('accounts:history')
        self.assertEqual(resolve(url).func, history_order)
        print(url)
        print(resolve(url))

    def test_category_new(self):
        url = reverse('accounts:category_new')
        self.assertEqual(resolve(url).func.view_class, CategoryCreateView)
        print(url)
        print(resolve(url))


class TestLoginForm(SimpleTestCase):
    """تست فرم لاگین """
    def test_valid_date(self):
        form = UserLoginForm(data={'email': 'jack@email.com', 'password': '123'})
        self.assertTrue(form.is_valid())

    def test_invalid_date(self):
        form = UserLoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)


class TestRegistrationForm(SimpleTestCase):
    """تست فرم رجیستر ذر صورا خالی بودن"""
    def test_invalid_date(self):
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)


class TestAddressForm(SimpleTestCase):
    """تست فرم آدرس"""
    def test_valid_date(self):
        form = AddressForm(data={'city': 'tehran', 'address': 'street', 'phone': '0912123'})
        self.assertTrue(form.is_valid())

    def test_invalid_date(self):
        form = AddressForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)


class TestViewProfile(TestCase):
    """تست ساخت پروفایل"""
    def setUp(self):
        self.client = User.objects.create_user('neda@email.com', 'neda', 'razi', '123')

    def test_user_profile(self):
        self.assertEqual(UserProfile.objects.count(), 1)




