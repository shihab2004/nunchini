# Generated by Django 3.2.5 on 2021-08-02 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='index_menu',
            name='img',
        ),
        migrations.AddField(
            model_name='index_menu',
            name='svg',
            field=models.TextField(blank=True, null=True),
        ),
    ]
