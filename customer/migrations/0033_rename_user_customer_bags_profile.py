# Generated by Django 3.2.5 on 2021-07-06 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0032_customer_bags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer_bags',
            old_name='user',
            new_name='profile',
        ),
    ]
