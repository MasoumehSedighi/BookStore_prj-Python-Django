# Generated by Django 3.2.6 on 2021-08-24 09:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True, verbose_name='عنوان')),
                ('slug', models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name='آدرس لینک')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='DiscountCash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(800)])),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DiscountPercent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('percentage', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, null=True, verbose_name='عنوان')),
                ('author', models.CharField(max_length=120, null=True, verbose_name='نویسنده')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد')),
                ('stock', models.PositiveIntegerField(verbose_name='موجودی')),
                ('image', models.ImageField(default='images/abc.jpg', null=True, upload_to='images/', verbose_name='عکس')),
                ('slug', models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name='آدرس لینک')),
                ('label', models.CharField(choices=[('new', 'جدید'), ('sale', 'حراج')], max_length=6, null=True, verbose_name='برچسب')),
                ('price', models.BigIntegerField(null=True, verbose_name='قیمت')),
                ('cash_discount', models.ForeignKey(blank=True, default=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cash', to='books.discountcash', verbose_name='تخفیف ریالی')),
                ('category', models.ManyToManyField(related_name='categories', to='books.Category', verbose_name='دسته بندی')),
                ('pers_discount', models.ForeignKey(blank=True, default=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='percent', to='books.discountpercent', verbose_name='تخفیف درصدی')),
            ],
            options={
                'verbose_name': 'کتاب',
                'verbose_name_plural': 'کتاب ها',
                'ordering': ['-created'],
            },
        ),
    ]
