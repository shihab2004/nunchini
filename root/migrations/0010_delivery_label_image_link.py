# Generated by Django 3.2.4 on 2021-06-21 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0009_delivery_label_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery_label',
            name='Image_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
