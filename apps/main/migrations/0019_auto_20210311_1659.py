# Generated by Django 2.2 on 2021-03-11 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_remove_slideraboutusone_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slideraboutusone',
            name='about_us',
        ),
        migrations.RemoveField(
            model_name='slideraboutusthree',
            name='about_us',
        ),
        migrations.RemoveField(
            model_name='slideraboutustwo',
            name='about_us',
        ),
    ]
