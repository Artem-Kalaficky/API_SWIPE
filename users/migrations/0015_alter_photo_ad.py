# Generated by Django 3.2 on 2022-09-13 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20220913_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='ad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='users.ad', verbose_name='Объявление'),
        ),
    ]
