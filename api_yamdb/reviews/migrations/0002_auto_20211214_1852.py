# Generated by Django 2.2.16 on 2021-12-14 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(choices=[(10, '10'), (9, '9'), (8, '8'), (7, '7'), (6, '6'), (5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1')], default=0),
        ),
    ]
