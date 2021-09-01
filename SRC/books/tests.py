
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from books.views import BookListView, SearchResultsListView, BookDetailView


class TestUrls(SimpleTestCase):
    def test_book_list(self):
        url = reverse('book:book_list')
        self.assertEqual(resolve(url).func.view_class, BookListView)
        print(url)
        print(resolve(url))

    def test_search_results(self):
        url = reverse('book:search_results')
        self.assertEqual(resolve(url).func.view_class, SearchResultsListView)
        print(url)
        print(resolve(url))

    def test_book_detail(self):
        url = reverse('book:book_detail', args=['book-test', ])
        self.assertEqual(resolve(url).func.view_class, BookDetailView)
        print(url)
        print(resolve(url))


