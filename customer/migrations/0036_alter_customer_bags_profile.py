# Generated by Django 3.2.5 on 2021-07-06 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0035_customer_bags_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_bags',
            name='profile',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='get_customerBag_item', to='customer.profile'),
        ),
    ]