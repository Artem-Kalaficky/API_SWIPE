# Generated by Django 3.2 on 2022-09-12 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='building',
            field=models.IntegerField(blank=True, null=True, verbose_name='Корпус'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='floor',
            field=models.IntegerField(blank=True, null=True, verbose_name='Этаж'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='number',
            field=models.IntegerField(blank=True, null=True, verbose_name='Номер'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='riser',
            field=models.IntegerField(blank=True, null=True, verbose_name='Стояк'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='section',
            field=models.IntegerField(blank=True, null=True, verbose_name='Секция'),
        ),
    ]
