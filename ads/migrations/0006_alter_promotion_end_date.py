# Generated by Django 3.2 on 2022-09-13 08:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0005_alter_promotion_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='end_date',
            field=models.DateField(default=datetime.date(2022, 10, 13), verbose_name='Дата завершения продвижения'),
        ),
    ]