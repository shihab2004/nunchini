# Generated by Django 3.2.5 on 2021-07-26 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0050_email_verify'),
    ]

    operations = [
        migrations.AddField(
            model_name='email_verify',
            name='email',
            field=models.EmailField(default='Jsad@sad.com', max_length=254),
            preserve_default=False,
        ),
    ]
