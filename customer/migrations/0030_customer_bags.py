# Generated by Django 3.2.5 on 2021-07-04 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0018_product_city'),
        ('customer', '0029_alter_user_adress_delivery_adress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer_bags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ManyToManyField(blank=True, to='Product.Product')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.profile')),
            ],
        ),
    ]