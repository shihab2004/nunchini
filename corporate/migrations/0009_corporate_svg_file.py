# Generated by Django 4.0.3 on 2022-03-30 17:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corporate', '0008_corporate_is_show_in_index_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporate',
            name='svg_file',
            field=models.FileField(blank=True, default=None, null=True, upload_to='corporate/svg', validators=[django.core.validators.FileExtensionValidator(['svg'])]),
        ),
    ]
