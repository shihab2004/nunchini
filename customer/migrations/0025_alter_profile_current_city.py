# Generated by Django 3.2.4 on 2021-06-27 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0042_area'),
        ('customer', '0024_profile_current_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='current_city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='get_current_profile', to='root.city'),
        ),
    ]