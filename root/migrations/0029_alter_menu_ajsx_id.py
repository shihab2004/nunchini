# Generated by Django 3.2.4 on 2021-06-23 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0028_menu_ajsx_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='ajsx_id',
            field=models.CharField(blank=True, help_text='It is the id of the menu .<strong>NO SPACE ALLOW</strong>. Please require the fill or it will auto fill from Menu name slug. <i>You can give any value<i>', max_length=30, null=True),
        ),
    ]
