# Generated by Django 3.2.4 on 2021-06-22 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0014_auto_20210622_0637'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=70)),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
            ],
        ),
        migrations.CreateModel(
            name='Mobile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=70)),
                ('Phone', models.PositiveIntegerField(max_length='11', verbose_name='Phone Number')),
            ],
        ),
        migrations.RemoveField(
            model_name='basic_setting',
            name='Email',
        ),
        migrations.RemoveField(
            model_name='basic_setting',
            name='Mobile',
        ),
        migrations.AddField(
            model_name='basic_setting',
            name='Email',
            field=models.ManyToManyField(blank=True, null=True, to='root.Email'),
        ),
        migrations.AddField(
            model_name='basic_setting',
            name='Mobile',
            field=models.ManyToManyField(blank=True, null=True, to='root.Mobile'),
        ),
    ]