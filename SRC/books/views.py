from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from books.models import Book, Category
from cart.forms import CartAddForm



class BookListView(ListView):
    """این متد لیست نمام کتاب ها را نشان میدهد"""
    paginate_by = 5
    model = Book
    template_name = 'books/book_list.html'

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['book_list'] = Book.objects.all()
        print(context)
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'books/home.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['cat_list'] = Category.objects.all()
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


def category_menu(request):
    category = request.GET.get('category')
    if category is None:
        books = Book.objects.all().order_by('-sold')[:6]
    else:
        books = Book.objects.filter(category__title=category)
    categories = Category.objects.all()
    context = {
        'books': books,
        'categories': categories
    }
    return render(request, 'books/home.html', context)
