# Generated by Django 4.0.3 on 2022-03-24 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0062_basic_setting_mini_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='basic_setting',
            name='Total_sell_money',
            field=models.BigIntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]
