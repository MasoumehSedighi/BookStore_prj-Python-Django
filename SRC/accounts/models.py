from .managers import UserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# Create your models here.

class Addresses(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    country = models.CharField(max_length=40, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    state = models.CharField(max_length=40, blank=True, null=True)
    street = models.CharField(max_length=40, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.country}-{self.city}-{self.state}-{self.street}'


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=20)
    country = models.CharField(max_length=40, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    state = models.CharField(max_length=40, blank=True, null=True)
    street = models.CharField(max_length=40, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=24, blank=True, null=True)
    card = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.full_name} {self.email}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def main_address(self):
        return f'{self.country}-{self.city}-{self.state}-{self.street}'


class Customer(User):
    class Meta:
        proxy = True
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتریان'


class Management(User):
    class Meta:
        proxy = True
        verbose_name = 'مدیر'
        verbose_name_plural = 'مدیران'


class Staff(User):
    class Meta:
        proxy = True
        verbose_name = 'کارمند'
        verbose_name_plural = 'کارمندان'
