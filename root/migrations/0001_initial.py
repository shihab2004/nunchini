# Generated by Django 3.2.4 on 2021-06-21 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='basic_setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(help_text='Please Enter your website name here', max_length=100)),
                ('Description', models.TextField()),
                ('Mobile', models.JSONField()),
                ('Email', models.JSONField()),
                ('Facebook', models.URLField()),
                ('Youtube', models.URLField()),
                ('Twitter', models.URLField()),
                ('Instagram', models.URLField()),
                ('Payment_allow', models.CharField(choices=[('Visa', 'Visa'), ('bKash', 'bKash'), ('Mastercard', 'Mastercard'), ('PayPal', 'PayPal'), ('Nagad', 'Nagad')], max_length=10)),
                ('delivery_allow', models.CharField(choices=[('CD', 'Cash on delivery'), ('DB', 'Delivery with banking')], max_length=2)),
                ('Play_store', models.URLField(blank=True, null=True)),
                ('App_store', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'BASIC SETTING',
                'db_table': 'BASIC SETTING',
            },
        ),
    ]
