from django.db import models

from users.models import House


class Advantage(models.Model):
    house = models.OneToOneField(House, on_delete=models.CASCADE, verbose_name='ЖК')
    advantage1 = models.BooleanField(default=True, verbose_name='Преимущество 1')
    advantage2 = models.BooleanField(default=False, verbose_name='Преимущество 2')

    class Meta:
        verbose_name = 'Преимущество'
        verbose_name_plural = 'Преимущества'


class Image(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name='ЖК', related_name='images')
    photo = models.ImageField(upload_to='gallery/', verbose_name='Фотография')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'


class News(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name='ЖК', related_name='news')
    name = models.CharField(max_length=32, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Document(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name='ЖК', related_name='documents')
    document = models.FileField(upload_to='files/', verbose_name='Документы')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


