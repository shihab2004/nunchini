# Generated by Django 3.2.5 on 2021-07-15 01:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0032_order_order_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='starts',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator(regex='^[0-5]')]),
        ),
    ]