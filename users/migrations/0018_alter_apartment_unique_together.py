# Generated by Django 3.2 on 2022-09-16 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20220916_1403'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='apartment',
            unique_together={('building', 'section', 'floor', 'riser', 'number', 'ad')},
        ),
    ]
