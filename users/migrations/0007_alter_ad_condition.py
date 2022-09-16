# Generated by Django 3.2 on 2022-09-12 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20220912_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='condition',
            field=models.CharField(choices=[('rough', 'Черновое'), ('residential', 'Жилое состояние')], default='rough', max_length=32, verbose_name='Жилое состояние'),
        ),
    ]
