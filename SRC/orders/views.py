from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from books.models import Book
from cart.cart import Cart
from orders.forms import CouponForm
from orders.models import Order, OrderItem, Coupon


# Create your views here.
@login_required
def detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = CouponForm()
    return render(request, 'order.html', {'order': order, 'form': form})


@login_required
def order_create(request):
    """ایجاد سفارش و کم کردن تعداد موجودی سبد از موجودی انبار"""
    cart = Cart(request)
    order = Order.objects.create(user=request.user, active=True)
    for item in cart:
        order_item = OrderItem.objects.create(order=order, book=item['book'],
                                              price=item['price'], quantity=item['quantity'], discount=item['discount'])

        book = Book.objects.get(id=order_item.book.id)
        if book.stock >= order_item.quantity:
            book.stock = book.stock - order_item.quantity
            book.save()
        else:
            messages.error(request, f'"{book.title} موجودی کافی نمیباشد /"', 'danger')
            return render(request, 'cart/detail.html', {'cart': cart})
    return redirect('orders:detail', order.id)


def coupon_apply(request, order_id):
    now = timezone.now()
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
            return redirect('orders:detail', order_id)
        except Coupon.DoesNotExist:
            messages.error(request, 'کد تخفیف نامعتبر میباشد ', 'danger')
            return redirect('orders:detail', order_id)


def complete_order(request):
    cart = Cart(request)
    order = Order.objects.get(user=request.user.id, active=True)
    message = "پرداخت با موفقیت انجام شد."
    order.active = False
    order.payment = True
    order.updated = timezone.now()
    order.save()
    cart.clear()
    context = {
        'message': message,
    }
    print(context)
    return render(request, 'order_complete.html', context)
