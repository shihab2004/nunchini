# Generated by Django 3.2.4 on 2021-06-26 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20210626_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_location',
            name='lat',
            field=models.DecimalField(decimal_places=3, max_digits=8),
        ),
        migrations.AlterField(
            model_name='user_location',
            name='long',
            field=models.DecimalField(decimal_places=3, max_digits=8),
        ),
    ]