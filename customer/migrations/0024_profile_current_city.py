# Generated by Django 3.2.4 on 2021-06-27 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0042_area'),
        ('customer', '0023_profile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='current_city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='root.city'),
        ),
    ]
