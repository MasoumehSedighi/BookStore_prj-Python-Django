from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from decimal import Decimal

# Create your models here.


class Category(models.Model):
    """ مدلی است که شامل گروه های کتابها میباشد و دو فیلد title برای نام دسته و slug برای آدرس لینک دارد """
    title = models.CharField(max_length=100, null=True, verbose_name='عنوان',)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name='آدرس لینک',)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book:category_menu', args={self.id})


class DiscountCash(models.Model):
    name = models.CharField(max_length=50, null=True, verbose_name='نام')
    amount = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(800)], verbose_name='مقدار')
    valid_from = models.DateTimeField(verbose_name='شروع')
    valid_to = models.DateTimeField(verbose_name='انقضا')
    active = models.BooleanField(default=False, verbose_name='فعال')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-valid_to']
        verbose_name = 'تخفیف - نقدی'
        verbose_name_plural = 'تخفیفات - نقدی'


class DiscountPercent(models.Model):
    name = models.CharField(max_length=50, null=True, verbose_name='نام')
    percentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='درصد')
    valid_from = models.DateTimeField(verbose_name='شزوع')
    valid_to = models.DateTimeField(verbose_name='انقضا')
    active = models.BooleanField(default=False, verbose_name='فعال')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-valid_to']
        verbose_name = 'تخفیف - درصدی'
        verbose_name_plural = 'تخفیفات - درصدی'


class Book(models.Model):

    NEW = 'new'
    SALE = 'sale'
    LABEL_CHOICES = (
        (NEW, 'جدید'),
        (SALE, 'حراج'),
    )
    title = models.CharField(max_length=150, null=True, verbose_name='عنوان',)
    category = models.ManyToManyField(Category, related_name='categories', verbose_name='دسته بندی')
    author = models.CharField(max_length=120,  null=True, verbose_name='نویسنده')
    created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد')
    stock = models.PositiveIntegerField(verbose_name='موجودی')
    image = models.ImageField(upload_to='images/', default='images/abc.jpg',  null=True, verbose_name='عکس')
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name='آدرس لینک',)
    label = models.CharField(choices=LABEL_CHOICES, max_length=6, null=True, default='None', verbose_name='برچسب')
    price = models.BigIntegerField(null=True, verbose_name='قیمت')
    cash_discount = models.ForeignKey(DiscountCash, on_delete=models.CASCADE, null=True,
                                      default=False, blank=True, related_name='cash', verbose_name='تخفیف ریالی',)
    pers_discount = models.ForeignKey(DiscountPercent, on_delete=models.CASCADE, null=True,
                                      default=False, blank=True, related_name='percent', verbose_name='تخفیف درصدی',)
    sold = models.PositiveIntegerField(default=0, verbose_name='فروخته شده')

    class Meta:
        ordering = ['-created']
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book:book_detail', args={self.slug})

    def reduce_stock(self, quantity):
        """با توجه به تعداد کالای انتخاب شده برای سفارش از تعداد موجودی کم میکند"""
        self.stock = self.stock - quantity
        print(quantity)
        self.save()
        return self.stock

    def add_stock(self, quantity):
        """با حدف کالا از سبد کالای انتخاب شده به تعداد موجودی اضافه میکند"""
        self.stock = self.stock + quantity
        self.save()
        return self.stock

    def get_item_discount(self):
        if self.cash_discount:
            discount = self.cash_discount.amount
            return Decimal(discount)
        if self.pers_discount:
            discount = (self.pers_discount.percentage / 100) * self.price
            return Decimal(discount)
        else:
            discount = 0
            return Decimal(discount)
