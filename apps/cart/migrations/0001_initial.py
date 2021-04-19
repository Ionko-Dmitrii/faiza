# Generated by Django 2.2 on 2021-04-14 12:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Формат номера! +996(555)123123', regex='^\\+996\\d{9}$')], verbose_name='Телефон')),
                ('comment', models.TextField(verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Оформление заказа',
                'verbose_name_plural': 'Оформление заказа',
            },
        ),
    ]
