from .managers import UserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save

""" new for address"""


class UserDefaultAddress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping = models.ForeignKey("Addresses", null=True, blank=True, on_delete=models.CASCADE,
                                 related_name="user_address_shipping_default")

    def __str__(self):
        return f'{self.user.email}'


class UserAddressManager(models.Manager):
    def get_shipping_addresses(self, user):
        return super(UserAddressManager, self).filter(default=True).filter(user=user)


"""finish new address"""


class Addresses(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name='آدرس')
    city = models.CharField(max_length=40, blank=True, null=True, verbose_name='شهر')
    phone = models.CharField(max_length=24, blank=True, null=True, verbose_name='تلفن')
    default = models.BooleanField(default=False, verbose_name='پیش فرض')
    objects = UserAddressManager()

    def __str__(self):
        return f'{self.city} - {self.address}'

    def __unicode__(self):
        return self.get_address()

    def get_address(self):
        return "%s, %s" % (self.address, self.city)

    class Meta:
        ordering = ['-city', ]


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=40, verbose_name='نام')
    last_name = models.CharField(max_length=20, verbose_name='نام خانوادگی')
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name='آدرس')
    city = models.CharField(max_length=40, blank=True, null=True, verbose_name='شهر')
    phone = models.CharField(max_length=24, blank=True, null=True, verbose_name='تلفن')
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    is_staff = models.BooleanField(default=False, verbose_name='کارمند')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.email}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


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


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    image = models.ImageField(blank=True, upload_to='images/users/', verbose_name='عکس پروفایل')
    comment = models.CharField(max_length=200, blank=True, null=True, verbose_name='نظرات')

    def __str__(self):
        return self.user.first_name

    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'


def save_profile_user(sender, **kwargs):
    if kwargs['created']:
        profile_user = UserProfile(user=kwargs['instance'])
        profile_user.save()


post_save.connect(save_profile_user, sender=User)
