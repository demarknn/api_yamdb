# Generated by Django 2.2.16 on 2022-03-09 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0016_auto_20220309_1526'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['-id']},
        ),
    ]
