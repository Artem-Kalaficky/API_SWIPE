# Generated by Django 3.2 on 2022-09-13 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_filter_status_of_house'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='number_of_rooms',
            field=models.CharField(choices=[('one-room', 'Однокомнатная'), ('two-room', 'Двухкомнатная'), ('three-room', 'Трехкомнатная')], default='one-room', max_length=32, verbose_name='Количество комнат'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='payment_option',
            field=models.CharField(choices=[('mortgage', 'Ипотека'), ('whole_amount', 'Оплата целиком')], default='mortgage', max_length=32, verbose_name='Варианты расчета'),
        ),
    ]
