# Generated by Django 3.2.4 on 2021-06-22 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='Product/')),
                ('image_link', models.URLField(blank=True, null=True)),
            ],
        ),
    ]