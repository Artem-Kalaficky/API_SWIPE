from allauth.account.models import EmailAddress
from django.core.management import BaseCommand
from faker import Faker

from api_swipe import settings
from users.models import UserProfile


fake = Faker('ru_RU')


def save(user):
    user.set_password('Zaqwerty123')
    user.save()
    EmailAddress.objects.create(
        user=user,
        email=user.email,
        primary=True,
        verified=True
    )


class Command(BaseCommand):
    help = 'Create users'

    def handle(self, *args, **kwargs):
        if not settings.DEBUG and not UserProfile.objects.filter(is_staff=False, is_developer=False).exists():
            for i in range(5):
                user = UserProfile.objects.create(
                    first_name=fake.first_name_male(),
                    last_name=fake.last_name_male(),
                    email=fake.email(),
                    telephone=f'+38 066 666 66 66'
                )
                save(user)
            self.stdout.write("Users successfully created")
        if not settings.DEBUG and not UserProfile.objects.filter(is_superuser=True).exists():
            user = UserProfile.objects.create(
                first_name='Иван',
                last_name='Иванов',
                email='admin@gmail.com',
                is_superuser=True,
                is_staff=True
            )
            save(user)
            self.stdout.write("Superuser successfully created")
