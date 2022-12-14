import re

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator, BaseValidator
from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('E-mail', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(default=timezone.now)
    first_name = models.CharField(max_length=64, blank=True, verbose_name='Имя', validators=[
        RegexValidator(
            regex=re.compile('[@_!#$%^&*<>?/\\\|}{~]'),
            message='Special characters are not allowed.',
            inverse_match=True
        )
    ])
    last_name = models.CharField(max_length=64, blank=True, verbose_name='Фамилия', validators=[
        RegexValidator(
            regex=re.compile('[@_!#$%^&*<>?/\\\|}{~]'),
            message='Special characters are not allowed.',
            inverse_match=True
        )
    ])
    telephone = PhoneNumberField(null=True, blank=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='gallery/', null=True, blank=True, verbose_name='Аватар')
    agent_first_name = models.CharField(max_length=64, null=True, blank=True, verbose_name='Имя агента', validators=[
        RegexValidator(
            regex=re.compile('[@_!#$%^&*<>?/\\\|}{~]'),
            message='Special characters are not allowed.',
            inverse_match=True
        )
    ])
    agent_last_name = models.CharField(max_length=64, null=True, blank=True, verbose_name='Фамилия агента', validators=[
        RegexValidator(
            regex=re.compile('[@_!#$%^&*<>?/\\\|}{~]'),
            message='Special characters are not allowed.',
            inverse_match=True
        )
    ])
    agent_telephone = PhoneNumberField(null=True, blank=True, verbose_name='Телефон агента')
    agent_email = models.EmailField(null=True, blank=True, verbose_name='E-mail агента')
    is_subscribed = models.BooleanField(default=False, verbose_name='Подписан?')
    is_auto_renewal = models.BooleanField(default=False, verbose_name='Автопродление')
    subscription_end_date = models.DateField(null=True, blank=True, verbose_name='Дата окончания подписки')
    to_me = models.BooleanField(default=True, verbose_name='Уведомления мне')
    to_me_and_agent = models.BooleanField(default=False, verbose_name='Уведомления мне и агенту')
    to_agent = models.BooleanField(default=False, verbose_name='Уведомления агенту')
    is_notices_disabled = models.BooleanField(default=False, verbose_name='Отключить уведомления')
    is_switch_to_agent = models.BooleanField(default=False, verbose_name='Переключить звонки и сообщения на агента')
    in_blacklist = models.BooleanField(default=False, verbose_name='В черном списке')
    houses = models.ManyToManyField('House', blank=True, verbose_name='Избранное(ЖК)')
    ads = models.ManyToManyField('Ad', blank=True, verbose_name='Избранное(Объявления)', related_name='favorites')
    is_developer = models.BooleanField(default=False, verbose_name='Застройщик?')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Filter(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Пользователь')
    TYPES = (('all', 'Все'),
             ('secondary', 'Вторичный рынок'),
             ('new_building', 'Новострой'),
             ('cottages', 'Коттеджы'))
    type = models.CharField(max_length=32, choices=TYPES, default='all', verbose_name='Тип фильтра')
    STATUSES = (('rented', 'Сдан'),
                ('free', 'Не сдан'))
    ROOMS = (('one-room', 'Однокомнатная'),
             ('two-room', 'Двухкомнатная'),
             ('three-room', 'Трехкомнатная'))
    number_of_rooms = models.CharField(max_length=32, choices=ROOMS, default='one-room', null=True, blank=True,
                                       verbose_name='Количество комнат')
    price_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена от',
                                     validators=[MinValueValidator(1)])
    price_up_to = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена до',
                                      validators=[MinValueValidator(1)])
    area_from = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='Площадь от',
                                    validators=[MinValueValidator(1)])
    area_up_to = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='Площадь до',
                                     validators=[MinValueValidator(1)])
    PURPOSES = (('apartment', 'Квартира'),
                ('penthouse', 'Пентхаус'))
    purpose = models.CharField(max_length=32, choices=PURPOSES, default='apartment', null=True, blank=True,
                               verbose_name='Назначение')
    TERMS = (('mortgage', 'Ипотека'),
             ('whole_amount', 'Оплата целиком'))
    purchase_term = models.CharField(max_length=32, choices=TERMS, default='mortgage', null=True, blank=True,
                                     verbose_name='Условия покупки')
    CONDITIONS = (('rough', 'Черновое'),
                  ('residential', 'Жилое состояние'))
    condition = models.CharField(max_length=32, choices=CONDITIONS, default='rough', null=True, blank=True,
                                 verbose_name='Состояние')
    is_save = models.BooleanField(default=False, verbose_name='Cохранить фильтр')

    class Meta:
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтры'
        unique_together = ['user', 'type']


class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender', verbose_name='Отправитель')
    recipient = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name='recipient',
                                  verbose_name='Получатель')
    message = models.TextField(verbose_name='Текст сообщения')
    image = models.ImageField(upload_to='gallery/', null=True, blank=True, verbose_name='Картинка')
    file = models.FileField(upload_to='files/', null=True, blank=True, verbose_name='Файл')
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Notary(models.Model):
    first_name = models.CharField(max_length=64, verbose_name='Имя', validators=[
        RegexValidator(
            regex=re.compile('[@_!#$%^&*<>?/\\\|}{~]'),
            message='Special characters are not allowed.',
            inverse_match=True
        )
    ])
    last_name = models.CharField(max_length=64, verbose_name='Фамилия', validators=[
        RegexValidator(
            regex=re.compile('[@_!#$%^&*<>?/\\\|}{~]'),
            message='Special characters are not allowed.',
            inverse_match=True
        )
    ])
    telephone = PhoneNumberField(null=True, blank=True, verbose_name='Телефон', unique=True)
    email = models.EmailField(verbose_name='E-mail', unique=True)
    avatar = models.ImageField(upload_to='gallery/', null=True, blank=True, verbose_name='Аватар')

    class Meta:
        verbose_name = 'Нотариус'
        verbose_name_plural = 'Нотариусы'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class House(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, verbose_name='Застройщик', null=True,
                                related_name='house')
    name = models.CharField(max_length=64, verbose_name='Название ЖК', validators=[
        RegexValidator(
            regex=re.compile('[@_!#$%^&*<>?/\\\|}{~]'),
            message='Special characters are not allowed.',
            inverse_match=True
        )
    ])
    address = models.CharField(max_length=64, verbose_name='Адрес ЖК', validators=[
        RegexValidator(
            regex=re.compile('[@_!#$%^&*<>?/\\\|}{~]'),
            message='Special characters are not allowed.',
            inverse_match=True
        )
    ])
    min_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Мин. цена')
    price_for_m2 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за m2')
    area_from = models.DecimalField(default=15, max_digits=6, decimal_places=2, verbose_name='Площади от')
    area_up_to = models.DecimalField(default=100, max_digits=6, decimal_places=2, verbose_name='Площади до')
    description = models.TextField(verbose_name='Описание ЖК', validators=[
        RegexValidator(
            regex=re.compile('[@_!#$%^&*<>?/\\\|}{~]'),
            message='Special characters are not allowed.',
            inverse_match=True
        )
    ])
    STATUSES = (('apartment', 'Квартиры'),)
    house_status = models.CharField(max_length=32, choices=STATUSES, default='apartment', verbose_name='Статус ЖК')
    TYPES = (('multi', 'Многоквартирный'),)
    house_type = models.CharField(max_length=32, choices=TYPES, default='multi', verbose_name='Вид ЖК')
    CLASSES = (('elite', 'Элитный'),)
    house_class = models.CharField(max_length=32, choices=CLASSES, default='elite', verbose_name='Класс ЖК')
    TECHNIQUES = (('monolithic', 'Монолитный каркас с керамзитом'),)
    building_technique = models.CharField(max_length=32, choices=TECHNIQUES, default='monolithic',
                                          verbose_name='Технология строительства')
    TERRITORIES = (('closed', 'Закрытая охраняемая'),)
    territory = models.CharField(max_length=32, choices=TERRITORIES, default='closed', verbose_name='Территория')
    distance_to_the_sea = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,
                                              verbose_name='Расстояние до моря')
    PAYMENTS = (('payments', 'Платежи'),)
    communal_payments = models.CharField(max_length=32, choices=PAYMENTS, default='payments',
                                         verbose_name='Коммунальные платежи')
    ceiling_height = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True,
                                         verbose_name='Высота потолков')
    CHOICES = (('yes', 'Да'),
               ('no', 'Нет'))
    gas = models.CharField(max_length=32, choices=CHOICES, default='yes', verbose_name='Газ')
    HEATING = (('central', 'Центральное'),)
    heating = models.CharField(max_length=32, choices=HEATING, default='central', verbose_name='Отопление')
    SEWERAGE = (('central', 'Центральная'),)
    type_of_sewerage = models.CharField(max_length=32, choices=SEWERAGE, default='central', verbose_name='Канализация')
    water_supply = models.CharField(max_length=32, choices=HEATING, default='central', verbose_name='Водоснабжение')
    AGREEMENTS = (('justice', 'Юстиция'),)
    agreements = models.CharField(max_length=32, choices=AGREEMENTS, default='justice', verbose_name='Оформление')
    OPTIONS = (('mortgage', 'Ипотека'),
               ('whole_amount', 'Оплата целиком'))
    payment_option = models.CharField(max_length=32, choices=OPTIONS, default='mortgage',
                                      verbose_name='Варианты расчета')
    PURPOSES = (('new_building', 'Новострой'),)
    house_purpose = models.CharField(max_length=32, choices=PURPOSES, default='new_building', verbose_name='Назначение')
    SUMS = (('full', 'Полная'),
            ('incomplete', 'Неполная'))
    amount_in_contract = models.CharField(max_length=32, choices=SUMS, default='full', verbose_name='Сумма в договоре')
    department_first_name = models.CharField(max_length=64, verbose_name='Имя', blank=True, validators=[
        RegexValidator(
            regex=re.compile('[@_!#$%^&*<>?/\\\|}{~]'),
            message='Special characters are not allowed.',
            inverse_match=True
        )
    ])
    department_last_name = models.CharField(max_length=64, verbose_name='Фамилия', blank=True, validators=[
        RegexValidator(
            regex=re.compile('[@_!#$%^&*<>?/\\\|}{~]'),
            message='Special characters are not allowed.',
            inverse_match=True
        )
    ])
    department_telephone = PhoneNumberField(null=True, blank=True, verbose_name='Телефон')
    department_email = models.EmailField(verbose_name='E-mail', blank=True)
    building = models.PositiveIntegerField(verbose_name='Количество корпусов', validators=[MaxValueValidator(4)])
    section = models.PositiveIntegerField(verbose_name='Количество секций', validators=[MaxValueValidator(4)])
    floor = models.PositiveIntegerField(verbose_name='Количество этажей', validators=[MaxValueValidator(50)])
    riser = models.PositiveIntegerField(verbose_name='Количество стояков', validators=[MaxValueValidator(4)])

    @property
    def main_photo(self):
        return self.images.all().first().photo.url

    class Meta:
        verbose_name = 'ЖК'
        verbose_name_plural = 'ЖК'

    def __str__(self):
        return self.name


class Ad(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='ad')
    address = models.CharField(max_length=64, verbose_name='Адрес', validators=[
        RegexValidator(
            regex=re.compile('[@_!#$%^&*<>?/\\\|}{~]'),
            message='Special characters are not allowed.',
            inverse_match=True
        )
    ])
    house = models.ForeignKey('House', on_delete=models.CASCADE, null=True, blank=True, verbose_name='ЖК')
    DOCUMENTS = (('property', 'Собственность'),)
    foundation_document = models.CharField(max_length=32, choices=DOCUMENTS, default='property', null=True, blank=True,
                                           verbose_name='Документ основания')
    PURPOSES = (('apartment', 'Квартира'),
                ('cottage', 'Коттедж'),
                ('new_building', 'Новострой'))
    purpose = models.CharField(max_length=32, choices=PURPOSES, default='apartment', verbose_name='Назначение')
    ROOMS = (('one-room', 'Однокомнатная'),
             ('two-room', 'Двухкомнатная'),
             ('three-room', 'Трехкомнатная'))
    number_of_rooms = models.CharField(max_length=32, choices=ROOMS, default='one-room',
                                       verbose_name='Количество комнат')
    LAYOUTS = (('studio', 'Студия'),)
    apartment_layout = models.CharField(max_length=32, choices=LAYOUTS, default='studio', null=True, blank=True,
                                        verbose_name='Планировка')
    CONDITIONS = (('rough', 'Черновое'),
                  ('residential', 'Жилое состояние'))
    condition = models.CharField(max_length=32, choices=CONDITIONS, default='rough', verbose_name='Жилое состояние')
    total_area = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Общая площадь',
                                     validators=[MinValueValidator(1)])
    kitchen_area = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,
                                       verbose_name='Площадь кухни', validators=[MinValueValidator(1)])
    CHOICES = (('yes', 'Да'),
               ('no', 'Нет'))
    balcony = models.CharField(max_length=32, choices=CHOICES, default='yes', null=True, blank=True,
                               verbose_name='Балкон/лоджия')
    TYPES = (('gas', 'Газовое отопление'),
             ('electric', 'Электроотопление'))
    heating_type = models.CharField(max_length=32, choices=TYPES, default='gas', null=True, blank=True,
                                    verbose_name='Тип отопления')
    OPTIONS = (('mortgage', 'Ипотека'),
               ('whole_amount', 'Оплата целиком'))
    payment_option = models.CharField(max_length=32, choices=OPTIONS, default='mortgage',
                                      verbose_name='Варианты расчета')
    agent_commission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                           verbose_name='Коммисия агенту')
    METHODS = (('email', 'Почта'),
               ('telephone', 'Звонок'))
    communication_method = models.CharField(max_length=32, choices=METHODS, default='email', null=True, blank=True,
                                            verbose_name='Способ связи')
    description = models.TextField(verbose_name='Описание', validators=[
        RegexValidator(
            regex=re.compile('[@_!#$%^&*<>?/\\\|}{~]'),
            message='Special characters are not allowed.',
            inverse_match=True
        )
    ])
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', validators=[MinValueValidator(1)])
    price_for_m2 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за m2')
    is_incorrect_price = models.BooleanField(default=False, verbose_name='Некорректная цена')
    is_incorrect_photo = models.BooleanField(default=False, verbose_name='Некорректное фото')
    is_incorrect_description = models.BooleanField(default=False, verbose_name='Некорректное описание')
    date_created = models.DateField(auto_now_add=True)
    is_disabled = models.BooleanField(default=False, verbose_name='Отклонено')

    @property
    def main_photo(self):
        return self.photos.all().first().photo.url

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-id']


class Photo(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name='Объявление', related_name='photos')
    photo = models.ImageField(upload_to='gallery/', verbose_name='Фото')
    order = models.IntegerField(verbose_name='Очередь')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ['order']


class Complaint(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='complaint', verbose_name='Объявление')
    text = models.TextField(verbose_name='Текст жалобы')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'


class Apartment(models.Model):
    ad = models.OneToOneField(Ad, on_delete=models.CASCADE, verbose_name='Объявление')
    building = models.PositiveIntegerField(verbose_name='Корпус', blank=True, null=True)
    section = models.PositiveIntegerField(verbose_name='Секция', blank=True, null=True)
    floor = models.PositiveIntegerField(verbose_name='Этаж', blank=True, null=True)
    riser = models.PositiveIntegerField(verbose_name='Стояк', blank=True, null=True)
    number = models.PositiveIntegerField(verbose_name='Номер', blank=True, null=True)
    schema = models.ImageField(upload_to='gallery/', null=True, blank=True, verbose_name='Планировка')
    is_reserved = models.BooleanField(default=False, verbose_name='Забронирована')

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'
        unique_together = ['building', 'section', 'floor', 'riser', 'number', 'ad']
        ordering = ['-id']




