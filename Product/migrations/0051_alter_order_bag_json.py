# Generated by Django 3.2.7 on 2021-09-16 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0050_auto_20210804_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='bag_json',
            field=models.TextField(),
        ),
    ]
