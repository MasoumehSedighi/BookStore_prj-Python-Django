from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from accounts.models import Addresses
from books.models import Book
from cart.cart import Cart
from orders.forms import CouponForm, AddressOrderForm
from orders.models import Order, OrderItem, Coupon


# Create your views here.
@login_required
def detail(request, order_id):

    order = get_object_or_404(Order, id=order_id)
    coupon_form = CouponForm()
    """گرفتن آدرس جدید و لیستی از آدرس های مشتری و آدرس دیفالت"""
    address_form = AddressOrderForm()
    current_addresses = Addresses.objects.filter(user=request.user)
    shipping_addresses = Addresses.objects.get_shipping_addresses(user=request.user)
    print(current_addresses)
    print(shipping_addresses)
    if request.method == "POST":
        """گرفتن آی دی آدرس انتخاب شده با نام تگ 'shipping_address' و ذخیره آن در فیل shipping_address آن سفارش"""
        shipping_a = request.POST['shipping_address']
        shipping_address_instance = Addresses.objects.get(id=shipping_a)
        order.shipping_address = shipping_address_instance
        order.active = False
        order.payment = True
        order.updated = timezone.now()
        order.save()
        return redirect('orders:complete_order', order_id)

    context = {
        'coupon_form': coupon_form,
        'order': order,
        "address_form": address_form,
        "order.id": order.id,
        "current_addresses": current_addresses,
        "shipping_addresses": shipping_addresses,

    }

    return render(request, 'order.html', context)


@login_required
def order_create(request):
    """ایجاد سفارش و کم کردن تعداد موجودی سبد از موجودی انبار"""
    cart = Cart(request)
    order = Order.objects.create(user=request.user, active=True)
    for item in cart:
        order_item = OrderItem.objects.create(order=order, book=item['book'],
                                              price=item['price'], quantity=item['quantity'], discount=item['discount'])

        book = Book.objects.get(id=order_item.book.id)
        """چک میکند اگر تعداد کالا از موجودی کمتر بود ار تعداد موجودی کم میکند"""
        if book.stock >= order_item.quantity:
            book.stock = book.stock - order_item.quantity
            book.sold = book.sold + order_item.quantity
            book.save()
            order.save()

        else:
            messages.error(request, f'"{book.title} موجودی کافی نمیباشد /"', 'danger')
            return render(request, 'cart/detail.html', {'cart': cart})
    return redirect('orders:detail', order.id)


def add_address(request, order_id):
    """گرفتن آدرس جدید در فرم ذر ثبت نهایی سفارش"""
    address_form = AddressOrderForm(request.POST)
    if address_form.is_valid():
        address = address_form.cleaned_data.get('address')
        city = address_form.cleaned_data.get('city')
        phone = address_form.cleaned_data.get('phone')
        address = Addresses.objects.create(user=request.user, address=address, city=city, phone=phone)
        address.save()
        return redirect('orders:detail', order_id)


def coupon_apply(request, order_id):
    """کرفتن کد کوپن تخفیف و جایگرینی مفدار آن در فیلذ تخفیف آن سفارش """
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


def complete_order(request, order_id):
    """مرحله آخر و تکمیل سفارش"""
    cart = Cart(request)
    order = Order.objects.get(user=request.user.id, id=order_id)
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
