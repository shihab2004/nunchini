# Generated by Django 3.2.4 on 2021-06-26 12:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0013_profile_user_adress_user_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='Phone',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(13)], verbose_name='Phone Number'),
        ),
    ]
