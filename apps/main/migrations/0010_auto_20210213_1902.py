# Generated by Django 2.2 on 2021-02-13 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20210213_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='portion_two',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Пол порции'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_two',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=14, null=True, verbose_name='Цена'),
        ),
    ]
