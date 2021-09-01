from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings
from accounts.models import Addresses
from books.models import Book

# Create your models here.


class Coupon(models.Model):
    code = models.CharField(unique=True, max_length=50, verbose_name='نام کد')
    valid_from = models.DateTimeField(verbose_name='شروع')
    valid_to = models.DateTimeField(verbose_name='انقضا')
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='درصد تخفیف')
    active = models.BooleanField(default=False, verbose_name='فعال')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'کد تخفیف ویژه'
        verbose_name_plural = 'کد تخفیف ویژه'


class Order(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name='کاریر')
    created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, null=True, verbose_name='تاریخ بروزرسانی')
    active = models.BooleanField(default=True, verbose_name='فعال')
    payment = models.BooleanField(default=False, verbose_name='پرداخت')
    discount = models.IntegerField(blank=True, null=True, default=None, verbose_name='تخفیف ویژه')
    shipping_address = models.ForeignKey(Addresses, on_delete=models.CASCADE, related_name='shipping_address', default=1)

    def __str__(self):
        return self.reference_number

    @property
    def reference_number(self):
        return f"ORDER-{self.pk}"

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            """در صورت تخفیف کپن از قیمت کل سفارش کم میکند"""
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سغارش')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='order_items', verbose_name='کتاب')
    price = models.IntegerField(verbose_name='قیمت')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='تعداد')
    discount = models.IntegerField(blank=True, null=True, default=None, verbose_name='تخفیف موردی')

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity - self.discount

    class Meta:
        verbose_name = 'جزییات سغارش '
        verbose_name_plural = 'جزییات سغارش'
