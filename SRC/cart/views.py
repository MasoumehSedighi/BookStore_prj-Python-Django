from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from books.models import Book
from .cart import Cart
from .forms import CartAddForm


# Create your views here.

def detail(request):
    """ جزییات سبذ موجود را به صفحه میفرستد """
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


@require_POST
def cart_add(request, book_id):
    """اطلاعات کتاب و تعداد آن را از کاربر میگیرد سشن cart  را میسازد و از طریق متد add به سبد اضافه میکند"""
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    form = CartAddForm(request.POST)
    if form.is_valid():
        cart_data = form.cleaned_data
        cart.add(book=book, quantity=cart_data['quantity'])
    return redirect('cart:detail')


def cart_remove(request, book_id):
    """ برای پاک کردن هر کتاب از سبد میباشد"""
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect('cart:detail')


