from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import FormMixin

from books.models import Book, DiscountCash, DiscountPercent
from cart.forms import CartAddForm


# class Home(TemplateView):
#     template_name = 'home.html'
#

class HomeListView(ListView):
    """این متد لیست نمام کتاب ها را در خانه نشان میدهد"""
    paginate_by = 4
    model = Book
    template_name = 'books/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        context['book_list'] = Book.objects.all()
        print(context)
        return context


class BookListView(ListView):
    """این متد لیست نمام کتاب ها را نشان میدهد"""
    model = Book
    template_name = 'books/book_list.html'

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['book_list'] = Book.objects.all()
        print(context)
        return context


class SearchResultsListView(ListView):
    """این کلاس مربوط به سرج کردن کناب و نویسنده میباشد"""
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')

        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )


class BookDetailView(FormMixin, DetailView):
    """جزییات هر کتاب را نشان میدهد"""
    model = Book
    template_name = 'books/book_detail.html'

    form_class = CartAddForm

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['form'] = CartAddForm(initial={'book': self.object})
        return context



