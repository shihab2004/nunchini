# Generated by Django 3.2.4 on 2021-06-26 02:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_auto_20210626_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_location',
            name='latitude',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(90), django.core.validators.MinValueValidator(-90)]),
        ),
        migrations.AlterField(
            model_name='user_location',
            name='longitude',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(180), django.core.validators.MinValueValidator(-180)]),
        ),
    ]