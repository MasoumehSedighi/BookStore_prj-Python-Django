from django.test import SimpleTestCase
from accounts.forms import UserRegistrationForm, UserLoginForm, AddressForm
from django.test import TestCase
from accounts.models import User
from accounts.models import UserProfile


# Create your tests here.


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





