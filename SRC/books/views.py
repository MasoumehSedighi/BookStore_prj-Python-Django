from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from books.models import Book
from cart.forms import CartAddForm


# Create your views here.

class HomeListView(ListView):
    """این متد لیست نمام کتاب ها را در خانه نشان میدهد"""
    paginate_by = 6
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
    template_name = 'books/staff_book_list.html'

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
        search = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
        if search:
            return search
        else:
            message = messages.info(self.request, 'نتیجه یافت نشد')
            return message


class BookDetailView(FormMixin, DetailView):
    """جزییات هر کتاب را نشان میدهد"""
    model = Book
    template_name = 'books/book_detail.html'

    form_class = CartAddForm

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['form'] = CartAddForm(initial={'book': self.object})
        return context



