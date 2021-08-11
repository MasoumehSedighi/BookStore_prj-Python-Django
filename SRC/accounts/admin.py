from django.contrib import admin

# Register your models here.
from .models import Customer, Addresses

admin.site.register(Customer)

admin.site.register(Addresses)
