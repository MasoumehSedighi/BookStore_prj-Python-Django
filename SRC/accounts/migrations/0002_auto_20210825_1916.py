# Generated by Django 3.2.6 on 2021-08-25 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='address',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='comment',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]