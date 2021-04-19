# Generated by Django 2.2 on 2021-04-15 17:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_auto_20210415_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(message='Формат номера! +996555123123', regex='^\\+996\\d{9}$')], verbose_name='Телефон'),
        ),
    ]
