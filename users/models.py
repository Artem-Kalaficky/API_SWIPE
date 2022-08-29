from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from ads.models import Promotion
from .managers import CustomUserManager


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('E-mail', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now)
    first_name = models.CharField(max_length=64, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=64, blank=True, verbose_name='Фамилия')
    telephone = PhoneNumberField(null=True, blank=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='gallery/', null=True, blank=True, verbose_name='Аватар')
    agent_first_name = models.CharField(max_length=64, null=True, blank=True, verbose_name='Имя агента')
    agent_last_name = models.CharField(max_length=64, null=True, blank=True, verbose_name='Фамилия агента')
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
    houses = models.ManyToManyField('House', verbose_name='Избранное(ЖК)')
    apartments = models.ManyToManyField('Apartment', verbose_name='Избранное(Апартаменты)')
    is_developer = models.BooleanField(default=False, verbose_name='Застройщик?')
    house = models.OneToOneField('House', on_delete=models.CASCADE, null=True, blank=True, related_name='house',
                                 verbose_name='ЖК')

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
    status_of_house = models.CharField(max_length=32, choices=STATUSES, default='rented', null=True, blank=True,
                                       verbose_name='Статус дома')
    district = models.CharField(max_length=32, null=True, blank=True, verbose_name='Район')
    microdistrict = models.CharField(max_length=32, null=True, blank=True, verbose_name='Микрорайон')
    ROOMS = (('one-room', 'Однокомнатная'),
             ('two-room', 'Двухкомнатная'),
             ('three-room', 'Трехкомнатная'))
    number_of_rooms = models.CharField(max_length=32, choices=ROOMS, default='one-room', null=True, blank=True,
                                       verbose_name='Количество комнат')
    price_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена от')
    price_up_to = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена до')
    area_from = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='Площадь от')
    area_up_to = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='Площадь до')
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

    class Meta:
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтры'


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
    first_name = models.CharField(max_length=64, verbose_name='Имя')
    last_name = models.CharField(max_length=64, verbose_name='Фамилия')
    telephone = PhoneNumberField(null=True, blank=True, verbose_name='Телефон')
    email = models.EmailField(verbose_name='E-mail')

    class Meta:
        verbose_name = 'Нотариус'
        verbose_name_plural = 'Нотариусы'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class House(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название ЖК')
    district = models.CharField(max_length=32, verbose_name='Район')
    address = models.CharField(max_length=64, verbose_name='Адрес ЖК')
    min_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Мин. цена')
    price_for_m2 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за m2')
    area = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Площади')
    description = models.TextField(verbose_name='Описание ЖК')
    STATUSES = (('None', ''),
                ('apartment', 'Квартиры'))
    house_status = models.CharField(max_length=32, choices=STATUSES, default='apartment', null=True, blank=True,
                                    verbose_name='Статус ЖК')
    TYPES = (('None', ''),
             ('multi', 'Многоквартирный'))
    house_type = models.CharField(max_length=32, choices=TYPES, default='multi', null=True, blank=True,
                                  verbose_name='Вид ЖК')
    CLASSES = (('None', ''),
               ('elite', 'Элитный'))
    house_class = models.CharField(max_length=32, choices=TYPES, default='elite', null=True, blank=True,
                                   verbose_name='Класс ЖК')
    TECHNIQUES = (('None', ''),
                  ('monolithic', 'Монолитный каркас с керамзитом'))
    building_technique = models.CharField(max_length=32, choices=TECHNIQUES, default='monolithic', null=True,
                                          blank=True, verbose_name='Технология строительства')
    TERRITORIES = (('None', ''),
                   ('closed', 'Закрытая охраняемая'))
    territory = models.CharField(max_length=32, choices=TERRITORIES, default='closed', null=True, blank=True,
                                 verbose_name='Территория')
    distance_to_the_sea = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,
                                              verbose_name='Расстояние до моря')
    PAYMENTS = (('None', ''),
                ('payments', 'Платежи'))
    communal_payments = models.CharField(max_length=32, choices=PAYMENTS, default='payments', null=True, blank=True,
                                         verbose_name='Коммунальные платежи')
    ceiling_height = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True,
                                         verbose_name='Высота потолков')
    CHOICES = (('yes', 'Да'),
               ('no', 'Нет'))
    gas = models.CharField(max_length=32, choices=CHOICES, default='yes', null=True, blank=True, verbose_name='Газ')
    HEATING = (('None', ''),
               ('central', 'Центральное'))
    heating = models.CharField(max_length=32, choices=HEATING, default='central', null=True, blank=True,
                               verbose_name='Отопление')
    SEWERAGE = (('None', ''),
                ('central', 'Центральная'))
    sewerage = models.CharField(max_length=32, choices=SEWERAGE, default='central', null=True, blank=True,
                                verbose_name='Канализация')
    water_supply = models.CharField(max_length=32, choices=HEATING, default='central', null=True, blank=True,
                                    verbose_name='Водоснабжение')
    AGREEMENTS = (('None', ''),
                  ('justice', 'Юстиция'))
    agreements = models.CharField(max_length=32, choices=AGREEMENTS, default='justice', null=True, blank=True,
                                  verbose_name='Оформление')
    OPTIONS = (('mortgage', 'Ипотека'),
               ('whole_amount', 'Оплата целиком'))
    payment_option = models.CharField(max_length=32, choices=OPTIONS, default='mortgage', null=True, blank=True,
                                      verbose_name='Варианты расчета')
    PURPOSES = (('None', ''),
                ('new_building', 'Новострой'))
    house_purpose = models.CharField(max_length=32, choices=PURPOSES, default='new_building', null=True, blank=True,
                                     verbose_name='Назначение')
    SUMS = (('full', 'Полная'),
            ('incomplete', 'Неполная'))
    amount_in_contract = models.CharField(max_length=32, choices=SUMS, default='full', null=True, blank=True,
                                          verbose_name='Сумма в договоре')
    department_first_name = models.CharField(max_length=64, verbose_name='Имя')
    department_last_name = models.CharField(max_length=64, verbose_name='Фамилия')
    department_telephone = PhoneNumberField(null=True, blank=True, verbose_name='Телефон')
    department_email = models.EmailField(verbose_name='E-mail')

    class Meta:
        verbose_name = 'ЖК'
        verbose_name_plural = 'ЖК'

    def __str__(self):
        return self.name


class Ad(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Пользователь')
    address = models.CharField(max_length=64, verbose_name='Адрес')
    house = models.OneToOneField('House', on_delete=models.CASCADE, null=True, blank=True, verbose_name='ЖК')
    DOCUMENTS = (('None', ''),
                 ('property', 'Собственность'))
    foundation_document = models.CharField(max_length=32, choices=DOCUMENTS, default='property', null=True, blank=True,
                                           verbose_name='Документ основания')
    PURPOSES = (('apartment', 'Квартира'),
                ('cottage', 'Коттедж'),
                ('new_building', 'Новострой'))
    purpose = models.CharField(max_length=32, choices=PURPOSES, default='apartment', null=True, blank=True,
                               verbose_name='Назначение')
    ROOMS = (('one-room', 'Однокомнатная'),
             ('two-room', 'Двухкомнатная'),
             ('three-room', 'Трехкомнатная'))
    number_of_rooms = models.CharField(max_length=32, choices=ROOMS, default='one-room', null=True, blank=True,
                                       verbose_name='Количество комнат')
    LAYOUTS = (('None', ''),
               ('studio', 'Студия'))
    apartment_layout = models.CharField(max_length=32, choices=LAYOUTS, default='studio', null=True, blank=True,
                                        verbose_name='Планировка')
    CONDITIONS = (('rough', 'Черновое'),
                  ('residential', 'Жилое состояние'))
    condition = models.CharField(max_length=32, choices=CONDITIONS, default='rough', null=True, blank=True,
                                 verbose_name='Жилое состояние')
    total_area = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,
                                     verbose_name='Общая площадь')
    kitchen_area = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,
                                       verbose_name='Площадь кухни')
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
    payment_option = models.CharField(max_length=32, choices=OPTIONS, default='mortgage', null=True, blank=True,
                                      verbose_name='Варианты расчета')
    agent_commission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                           verbose_name='Коммисия агенту')
    METHODS = (('email', 'Почта'),
               ('telephone', 'Звонок'))
    communication_method = models.CharField(max_length=32, choices=METHODS, default='email', null=True, blank=True,
                                            verbose_name='Способ связи')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    is_incorrect_price = models.BooleanField(default=False, verbose_name='Некорректная цена')
    is_incorrect_photo = models.BooleanField(default=False, verbose_name='Некорректное фото')
    is_incorrect_description = models.BooleanField(default=False, verbose_name='Некорректное описание')
    date_created = models.DateField(auto_now_add=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.PROTECT, null=True, blank=True,
                                  verbose_name='Продвижение')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Photo(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name='Объявление')
    photo = models.ImageField(upload_to='gallery/', verbose_name='Фото')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'


class Apartment(models.Model):
    ad = models.OneToOneField(Ad, on_delete=models.PROTECT, verbose_name='Объявление')
    building = models.IntegerField(verbose_name='Корпус')
    section = models.IntegerField(verbose_name='Секция')
    floor = models.IntegerField(verbose_name='Этаж')
    riser = models.IntegerField(verbose_name='Стояк')
    number = models.IntegerField(verbose_name='Номер')
    is_reserved = models.BooleanField(default=False, verbose_name='Забронирована')

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'

