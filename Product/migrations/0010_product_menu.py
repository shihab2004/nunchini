# Generated by Django 3.2.4 on 2021-06-23 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0029_alter_menu_ajsx_id'),
        ('Product', '0009_alter_product_image_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='root.menu'),
        ),
    ]