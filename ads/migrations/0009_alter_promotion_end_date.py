# Generated by Django 3.2 on 2022-10-12 09:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0008_alter_promotion_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='end_date',
            field=models.DateField(default=datetime.date(2022, 11, 11), verbose_name='Дата завершения продвижения'),
        ),
    ]