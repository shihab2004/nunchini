# Generated by Django 3.2.6 on 2021-08-02 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corporate', '0007_alter_corporate_customer_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporate',
            name='is_show_in_index_page',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
