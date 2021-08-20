from django.contrib.auth.base_user import BaseUserManager
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


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, password, last_name):
        if not email:
            raise ValueError('user must have a email address')
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, email, first_name, password, last_name):
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password, last_name):
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


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
