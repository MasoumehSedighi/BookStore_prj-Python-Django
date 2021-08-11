from django.contrib import admin

# Register your models here.
from .models import Order, OrderItems, Cart, Coupon

admin.site.register(Order)

admin.site.register(OrderItems)

admin.site.register(Cart)

admin.site.register(Coupon)
