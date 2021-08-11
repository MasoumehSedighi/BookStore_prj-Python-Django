from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from books.models import Book


# Create your models here.

class Coupon(models.Model):
    code = models.CharField(unique=True, max_length=50)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.code


class Cart(models.Model):
    user = models.ForeignKey('accounts.Customer', blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)


class Order(models.Model):
    STATUS = (
            ('order', 'سفارش'),
            ('submitted', 'ثبت')
        )

    PAY_CHOICES = (
        ('pending', 'Pending'),
        ('failed', 'Failed'),
        ('completed', 'Completed')
    )
    user = models.ForeignKey('accounts.Customer', blank=True, null=True, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, blank=True, null=True, on_delete=models.CASCADE )
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField( null=True)
    address = models.CharField(max_length=250, null=True)
    postal_code = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=100, null=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    total = models.BigIntegerField( null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='order', null=True)
    payment = models.CharField(max_length=10, choices=PAY_CHOICES, default='pending', null=True)

    def __str__(self):
        return self.reference_number

    @property
    def reference_number(self):
        return f"ORDER-{self.pk}"


class OrderItems(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, blank=True, null=True, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()



