# Generated by Django 2.2.16 on 2022-03-09 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0011_auto_20220309_1137'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]