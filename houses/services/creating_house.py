import random

from houses.models import Advantage
from users.models import House


def create_house(instance):
    House.objects.create(
        user=instance,
        name=f'ЖК "{instance.first_name}"',
        address='ул. Тестовая 1',
        min_price=100000,
        price_for_m2=1000,
        description='Какое-то описание',
        building=random.randint(1, 4),
        section=random.randint(1, 4),
        floor=random.randint(1, 20),
        riser=random.randint(1, 4),
    )


def create_advantage(instance):
    Advantage.objects.create(
        house=instance
    )
