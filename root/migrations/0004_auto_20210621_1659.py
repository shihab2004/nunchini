# Generated by Django 3.2.4 on 2021-06-21 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0003_auto_20210621_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment_options_allow',
            name='Image_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='payment_options_allow',
            name='Image',
            field=models.ImageField(blank=True, null=True, upload_to='payment_options'),
        ),
    ]
