# Generated by Django 3.2.6 on 2021-08-29 20:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'پروفایل', 'verbose_name_plural': 'پروفایل ها'},
        ),
        migrations.AlterField(
            model_name='addresses',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='addresses',
            name='city',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='شهر'),
        ),
        migrations.AlterField(
            model_name='addresses',
            name='default',
            field=models.BooleanField(default=False, verbose_name='پیش فرض'),
        ),
        migrations.AlterField(
            model_name='addresses',
            name='phone',
            field=models.CharField(blank=True, max_length=24, null=True, verbose_name='تلفن'),
        ),
        migrations.AlterField(
            model_name='addresses',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='شهر'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=40, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='ادمین'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='کارمند'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=20, verbose_name='نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=24, null=True, verbose_name='تلفن'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='comment',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='نظرات'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/users/', verbose_name='عکس پروفایل'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]
