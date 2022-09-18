# Generated by Django 3.2 on 2022-09-09 16:28

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateField(default=django.utils.timezone.now)),
                ('first_name', models.CharField(blank=True, max_length=64, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=64, verbose_name='Фамилия')),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Телефон')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='gallery/', verbose_name='Аватар')),
                ('agent_first_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='Имя агента')),
                ('agent_last_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='Фамилия агента')),
                ('agent_telephone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Телефон агента')),
                ('agent_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail агента')),
                ('is_subscribed', models.BooleanField(default=False, verbose_name='Подписан?')),
                ('is_auto_renewal', models.BooleanField(default=False, verbose_name='Автопродление')),
                ('subscription_end_date', models.DateField(blank=True, null=True, verbose_name='Дата окончания подписки')),
                ('to_me', models.BooleanField(default=True, verbose_name='Уведомления мне')),
                ('to_me_and_agent', models.BooleanField(default=False, verbose_name='Уведомления мне и агенту')),
                ('to_agent', models.BooleanField(default=False, verbose_name='Уведомления агенту')),
                ('is_notices_disabled', models.BooleanField(default=False, verbose_name='Отключить уведомления')),
                ('is_switch_to_agent', models.BooleanField(default=False, verbose_name='Переключить звонки и сообщения на агента')),
                ('in_blacklist', models.BooleanField(default=False, verbose_name='В черном списке')),
                ('is_developer', models.BooleanField(default=False, verbose_name='Застройщик?')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=64, verbose_name='Адрес')),
                ('foundation_document', models.CharField(blank=True, choices=[('None', ''), ('property', 'Собственность')], default='property', max_length=32, null=True, verbose_name='Документ основания')),
                ('purpose', models.CharField(choices=[('apartment', 'Квартира'), ('cottage', 'Коттедж'), ('new_building', 'Новострой')], default='apartment', max_length=32, verbose_name='Назначение')),
                ('number_of_rooms', models.CharField(blank=True, choices=[('one-room', 'Однокомнатная'), ('two-room', 'Двухкомнатная'), ('three-room', 'Трехкомнатная')], default='one-room', max_length=32, null=True, verbose_name='Количество комнат')),
                ('apartment_layout', models.CharField(blank=True, choices=[('None', ''), ('studio', 'Студия')], default='studio', max_length=32, null=True, verbose_name='Планировка')),
                ('condition', models.CharField(blank=True, choices=[('rough', 'Черновое'), ('residential', 'Жилое состояние')], default='rough', max_length=32, null=True, verbose_name='Жилое состояние')),
                ('total_area', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Общая площадь')),
                ('kitchen_area', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Площадь кухни')),
                ('balcony', models.CharField(blank=True, choices=[('yes', 'Да'), ('no', 'Нет')], default='yes', max_length=32, null=True, verbose_name='Балкон/лоджия')),
                ('heating_type', models.CharField(blank=True, choices=[('gas', 'Газовое отопление'), ('electric', 'Электроотопление')], default='gas', max_length=32, null=True, verbose_name='Тип отопления')),
                ('payment_option', models.CharField(blank=True, choices=[('mortgage', 'Ипотека'), ('whole_amount', 'Оплата целиком')], default='mortgage', max_length=32, null=True, verbose_name='Варианты расчета')),
                ('agent_commission', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Коммисия агенту')),
                ('communication_method', models.CharField(blank=True, choices=[('email', 'Почта'), ('telephone', 'Звонок')], default='email', max_length=32, null=True, verbose_name='Способ связи')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Цена')),
                ('is_incorrect_price', models.BooleanField(default=False, verbose_name='Некорректная цена')),
                ('is_incorrect_photo', models.BooleanField(default=False, verbose_name='Некорректное фото')),
                ('is_incorrect_description', models.BooleanField(default=False, verbose_name='Некорректное описание')),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
            },
        ),
        migrations.CreateModel(
            name='Notary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=64, verbose_name='Фамилия')),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='gallery/', verbose_name='Аватар')),
            ],
            options={
                'verbose_name': 'Нотариус',
                'verbose_name_plural': 'Нотариусы',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='gallery/', verbose_name='Фото')),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.ad', verbose_name='Объявление')),
            ],
            options={
                'verbose_name': 'Фото',
                'verbose_name_plural': 'Фото',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Текст сообщения')),
                ('image', models.ImageField(blank=True, null=True, upload_to='gallery/', verbose_name='Картинка')),
                ('file', models.FileField(blank=True, null=True, upload_to='files/', verbose_name='Файл')),
                ('date', models.DateField(auto_now_add=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipient', to=settings.AUTH_USER_MODEL, verbose_name='Получатель')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название ЖК')),
                ('address', models.CharField(max_length=64, verbose_name='Адрес ЖК')),
                ('min_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Мин. цена')),
                ('price_for_m2', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена за m2')),
                ('area_from', models.DecimalField(decimal_places=2, default=15, max_digits=6, verbose_name='Площади от')),
                ('area_up_to', models.DecimalField(decimal_places=2, default=100, max_digits=6, verbose_name='Площади до')),
                ('description', models.TextField(verbose_name='Описание ЖК')),
                ('house_status', models.CharField(choices=[('apartment', 'Квартиры')], default='apartment', max_length=32, verbose_name='Статус ЖК')),
                ('house_type', models.CharField(choices=[('multi', 'Многоквартирный')], default='multi', max_length=32, verbose_name='Вид ЖК')),
                ('house_class', models.CharField(choices=[('elite', 'Элитный')], default='elite', max_length=32, verbose_name='Класс ЖК')),
                ('building_technique', models.CharField(choices=[('monolithic', 'Монолитный каркас с керамзитом')], default='monolithic', max_length=32, verbose_name='Технология строительства')),
                ('territory', models.CharField(choices=[('closed', 'Закрытая охраняемая')], default='closed', max_length=32, verbose_name='Территория')),
                ('distance_to_the_sea', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Расстояние до моря')),
                ('communal_payments', models.CharField(choices=[('payments', 'Платежи')], default='payments', max_length=32, verbose_name='Коммунальные платежи')),
                ('ceiling_height', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='Высота потолков')),
                ('gas', models.CharField(choices=[('yes', 'Да'), ('no', 'Нет')], default='yes', max_length=32, verbose_name='Газ')),
                ('heating', models.CharField(choices=[('central', 'Центральное')], default='central', max_length=32, verbose_name='Отопление')),
                ('type_of_sewerage', models.CharField(choices=[('central', 'Центральная')], default='central', max_length=32, verbose_name='Канализация')),
                ('water_supply', models.CharField(choices=[('central', 'Центральное')], default='central', max_length=32, verbose_name='Водоснабжение')),
                ('agreements', models.CharField(choices=[('justice', 'Юстиция')], default='justice', max_length=32, verbose_name='Оформление')),
                ('payment_option', models.CharField(choices=[('mortgage', 'Ипотека'), ('whole_amount', 'Оплата целиком')], default='mortgage', max_length=32, verbose_name='Варианты расчета')),
                ('house_purpose', models.CharField(choices=[('new_building', 'Новострой')], default='new_building', max_length=32, verbose_name='Назначение')),
                ('amount_in_contract', models.CharField(choices=[('full', 'Полная'), ('incomplete', 'Неполная')], default='full', max_length=32, verbose_name='Сумма в договоре')),
                ('department_first_name', models.CharField(blank=True, max_length=64, verbose_name='Имя')),
                ('department_last_name', models.CharField(blank=True, max_length=64, verbose_name='Фамилия')),
                ('department_telephone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Телефон')),
                ('department_email', models.EmailField(blank=True, max_length=254, verbose_name='E-mail')),
                ('building', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(4)], verbose_name='Количество корпусов')),
                ('section', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(4)], verbose_name='Количество секций')),
                ('floor', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(50)], verbose_name='Количество этажей')),
                ('riser', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(4)], verbose_name='Количество стояков')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='house', to=settings.AUTH_USER_MODEL, verbose_name='Застройщик')),
            ],
            options={
                'verbose_name': 'ЖК',
                'verbose_name_plural': 'ЖК',
            },
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('all', 'Все'), ('secondary', 'Вторичный рынок'), ('new_building', 'Новострой'), ('cottages', 'Коттеджы')], default='all', max_length=32, verbose_name='Тип фильтра')),
                ('status_of_house', models.CharField(blank=True, choices=[('rented', 'Сдан'), ('free', 'Не сдан')], default='rented', max_length=32, null=True, verbose_name='Статус дома')),
                ('number_of_rooms', models.CharField(blank=True, choices=[('one-room', 'Однокомнатная'), ('two-room', 'Двухкомнатная'), ('three-room', 'Трехкомнатная')], default='one-room', max_length=32, null=True, verbose_name='Количество комнат')),
                ('price_from', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена от')),
                ('price_up_to', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена до')),
                ('area_from', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Площадь от')),
                ('area_up_to', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Площадь до')),
                ('purpose', models.CharField(blank=True, choices=[('apartment', 'Квартира'), ('penthouse', 'Пентхаус')], default='apartment', max_length=32, null=True, verbose_name='Назначение')),
                ('purchase_term', models.CharField(blank=True, choices=[('mortgage', 'Ипотека'), ('whole_amount', 'Оплата целиком')], default='mortgage', max_length=32, null=True, verbose_name='Условия покупки')),
                ('condition', models.CharField(blank=True, choices=[('rough', 'Черновое'), ('residential', 'Жилое состояние')], default='rough', max_length=32, null=True, verbose_name='Состояние')),
                ('is_save', models.BooleanField(default=False, verbose_name='Cохранить фильтр')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Фильтр',
                'verbose_name_plural': 'Фильтры',
            },
        ),
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.IntegerField(verbose_name='Корпус')),
                ('section', models.IntegerField(verbose_name='Секция')),
                ('floor', models.IntegerField(verbose_name='Этаж')),
                ('riser', models.IntegerField(verbose_name='Стояк')),
                ('number', models.IntegerField(verbose_name='Номер')),
                ('is_reserved', models.BooleanField(default=False, verbose_name='Забронирована')),
                ('ad', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='users.ad', verbose_name='Объявление')),
            ],
            options={
                'verbose_name': 'Квартира',
                'verbose_name_plural': 'Квартиры',
            },
        ),
        migrations.AddField(
            model_name='ad',
            name='house',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.house', verbose_name='ЖК'),
        ),
        migrations.AddField(
            model_name='ad',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ad', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='apartments',
            field=models.ManyToManyField(blank=True, to='users.Apartment', verbose_name='Избранное(Апартаменты)'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='houses',
            field=models.ManyToManyField(blank=True, to='users.House', verbose_name='Избранное(ЖК)'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]