# Generated by Django 3.2.6 on 2021-09-02 02:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=40, verbose_name='نام')),
                ('last_name', models.CharField(max_length=20, verbose_name='نام خانوادگی')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='آدرس')),
                ('city', models.CharField(blank=True, max_length=40, null=True, verbose_name='شهر')),
                ('phone', models.CharField(blank=True, max_length=24, null=True, verbose_name='تلفن')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='ایمیل')),
                ('is_staff', models.BooleanField(default=False, verbose_name='کارمند')),
                ('is_admin', models.BooleanField(default=False, verbose_name='ادمین')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Addresses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='آدرس')),
                ('city', models.CharField(blank=True, max_length=40, null=True, verbose_name='شهر')),
                ('phone', models.CharField(blank=True, max_length=24, null=True, verbose_name='تلفن')),
                ('default', models.BooleanField(default=False, verbose_name='پیش فرض')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'ordering': ['-city'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='images/', verbose_name='عکس پروفایل')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پروفایل',
                'verbose_name_plural': 'پروفایل ها',
            },
        ),
        migrations.CreateModel(
            name='UserDefaultAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping', models.ForeignKey(blank=True, default='images/abc.jpg', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_address_shipping_default', to='accounts.addresses')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
            ],
            options={
                'verbose_name': 'مشتری',
                'verbose_name_plural': 'مشتریان',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
        ),
        migrations.CreateModel(
            name='Management',
            fields=[
            ],
            options={
                'verbose_name': 'مدیر',
                'verbose_name_plural': 'مدیران',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
            ],
            options={
                'verbose_name': 'کارمند',
                'verbose_name_plural': 'کارمندان',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
        ),
    ]
