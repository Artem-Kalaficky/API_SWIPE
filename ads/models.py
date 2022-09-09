from datetime import timedelta

from django.db import models
from django.utils import timezone

from users.models import Ad


class Promotion(models.Model):
    ad = models.OneToOneField(Ad, on_delete=models.CASCADE, verbose_name='Объявление')
    is_gift = models.BooleanField(default=False, verbose_name='Подарок при покупке')
    is_bargaining = models.BooleanField(default=False, verbose_name='Возможен торг')
    is_by_the_sea = models.BooleanField(default=False, verbose_name='Квартира у моря')
    is_sleeping_area = models.BooleanField(default=False, verbose_name='В спальном районе')
    is_nice_price = models.BooleanField(default=False, verbose_name='Вам повезло с ценой')
    is_for_big_family = models.BooleanField(default=False, verbose_name='Для большой семьи')
    is_family_home = models.BooleanField(default=False, verbose_name='Семейное гнездышко')
    is_private_parking = models.BooleanField(default=False, verbose_name='Отдельная парковка')
    COLORS = (('None', ''),
              ('red', 'Красный'),
              ('green', 'Зелёный'))
    color = models.CharField(max_length=32, choices=COLORS, default='None', null=True, blank=True,
                             verbose_name='Выделить цветом')
    TYPES = (('None', ''),
             ('big', 'Большое объявление'),
             ('raise', 'Поднять объявление'),
             ('turbo', 'Турбо'))
    type_of_promotion = models.CharField(max_length=32, choices=TYPES, default='None', null=True, blank=True,
                                         verbose_name='Тип объявления')
    end_date = models.DateField(default=(timezone.now().date() + timedelta(days=30)),
                                verbose_name='Дата завершения продвижения')

    class Meta:
        verbose_name = 'Продвижение'
        verbose_name_plural = 'Продвижения'

