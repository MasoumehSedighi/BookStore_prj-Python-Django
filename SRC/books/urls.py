from django.conf.urls import url
from django.urls import path, re_path
from books.views import BookListView, SearchResultsListView, BookDetailView, HomeListView, CategoryListView

app_name = 'book'
urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('list', BookListView.as_view(), name='book_list'),
    path('category', CategoryListView.as_view(), name='category_list'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
    re_path(r'detail/(?P<slug>[-\w]+)/', BookDetailView.as_view(), name='book_detail'),
    # path('categories/', CategoryView.as_view(), name='categories'),
    # path('details/<str:pk>/', CategoriesDetailView.as_view(), name='categories_detail'),
]