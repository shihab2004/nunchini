# Generated by Django 3.2.5 on 2021-08-02 00:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0054_alter_user_location_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_location',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location', to='customer.profile'),
        ),
    ]
