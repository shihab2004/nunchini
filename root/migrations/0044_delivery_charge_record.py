# Generated by Django 3.2.5 on 2021-07-10 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0043_alter_area_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery_Charge_record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_price', models.PositiveIntegerField()),
                ('delivery_Charge', models.PositiveIntegerField()),
            ],
        ),
    ]