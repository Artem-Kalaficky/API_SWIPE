# Generated by Django 3.2 on 2022-09-12 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220912_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='schema',
            field=models.ImageField(blank=True, null=True, upload_to='gallery/', verbose_name='Планировка'),
        ),
    ]
