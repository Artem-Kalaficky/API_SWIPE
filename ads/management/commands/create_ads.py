from random import choice

from django.core.management import BaseCommand

from api_swipe import settings
from users.models import UserProfile, Ad, House


class Command(BaseCommand):
    help = 'Create ads for feed and apartments'

    def handle(self, *args, **kwargs):
        if not settings.DEBUG and not Ad.objects.all().exists():
            users = UserProfile.objects.filter(is_staff=False, is_developer=False)
            houses = House.objects.all()
            purposes = ['apartment', 'new_building']
            rooms = ['one-room', 'three-room', 'two-room']
            conditions = ['rough', 'residential']
            layouts = ['studio']
            payments = ['mortgage', 'whole_amount']
            for i in range(30):
                price = choice([600000, 2300000, 10000000, 400000, 55000])
                total_area = choice([38, 55, 66, 90])
                price_for_m2 = price / total_area
                Ad.objects.create(
                    house=choice(houses),
                    user=choice(users),
                    address='test address 1',
                    purpose=choice(purposes),
                    number_of_rooms=choice(rooms),
                    apartment_layout=choice(layouts),
                    total_area=total_area,
                    kitchen_area=choice([5, 10, 12, 17]),
                    condition=choice(conditions),
                    payment_option=choice(payments),
                    description='Very interesting description!',
                    agent_commission=10000,
                    price=price,
                    price_for_m2=price_for_m2
                )
            self.stdout.write("Ads successfully created")
