from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import user_register, BookDeleteView, BookListView


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
        url = reverse('accounts:book_delete', args=['5',])
        self.assertEqual(resolve(url).func.view_class, BookDeleteView)
        print(url)
        print(resolve(url))
