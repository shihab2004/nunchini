# Generated by Django 3.2.4 on 2021-06-23 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0011_remove_product_menu'),
        ('root', '0030_menu_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='products',
            field=models.ManyToManyField(blank=True, to='Product.Product'),
        ),
    ]
