# Generated by Django 4.0.3 on 2022-03-31 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0072_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='is_new',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
