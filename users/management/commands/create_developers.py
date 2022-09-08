from allauth.account.models import EmailAddress
from django.core.management import BaseCommand
from faker import Faker

from api_swipe import settings
from users.models import UserProfile


fake = Faker('ru_RU')


class Command(BaseCommand):
    help = 'Create developers'

    def handle(self, *args, **kwargs):
        if not settings.DEBUG and not UserProfile.objects.filter(is_staff=False, is_developer=True).exists():
            for i in range(2):
                user = UserProfile.objects.create(
                    is_developer=True,
                    first_name=fake.first_name_male(),
                    last_name=fake.last_name_male(),
                    email=fake.email(),
                    telephone=f'+38 066 666 66 66'
                )
                user.set_password('Zaqwerty123')
                user.save()
                EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
            self.stdout.write("Developers successfully created")
