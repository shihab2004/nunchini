# Generated by Django 3.2.4 on 2021-06-22 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0024_auto_20210622_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='Date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]