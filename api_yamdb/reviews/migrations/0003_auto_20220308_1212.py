# Generated by Django 2.2.16 on 2022-03-08 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220308_1103'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviews',
            old_name='rating',
            new_name='score',
        ),
    ]
