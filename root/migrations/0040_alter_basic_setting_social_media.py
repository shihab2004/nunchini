# Generated by Django 3.2.4 on 2021-06-26 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0039_auto_20210626_0559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basic_setting',
            name='Social_media',
            field=models.ManyToManyField(blank=True, to='root.social_media'),
        ),
    ]