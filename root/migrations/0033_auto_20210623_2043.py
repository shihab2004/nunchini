# Generated by Django 3.2.4 on 2021-06-23 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0032_remove_menu_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='Sub_Menu',
        ),
        migrations.AddField(
            model_name='menu',
            name='parent',
            field=models.PositiveIntegerField(blank=True, help_text='Parent Menu id', null=True),
        ),
    ]
