from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Book(models.Model):
    NEW = 'new'
    SALE = 'sale'
    LABEL_CHOICES = (
        (NEW, 'جدید'),
        (SALE, 'حراج'),
    )
    title = models.CharField(max_length=150, null=True)
    category = models.ManyToManyField(Category, related_name='books')
    author = models.CharField(max_length=120,  null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    stock = models.CharField(max_length=10)
    image = models.ImageField(upload_to='images/', default='images/abc.jpg',  null=True)
    slug = models.SlugField(max_length=255, null=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=6, null=True)
    price = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    discount_price = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title

