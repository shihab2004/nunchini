# Generated by Django 3.2.5 on 2021-07-17 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0002_support_menu_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='support_menu',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]