# Generated by Django 5.1.7 on 2025-03-14 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='users',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
