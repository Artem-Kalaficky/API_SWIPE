from allauth.account.models import EmailAddress
from django.core.management import BaseCommand
from faker import Faker

from api_swipe import settings
from users.models import Notary, UserProfile


fake = Faker('ru_RU')


class Command(BaseCommand):
    help = 'Init data to raise the project'

    def handle(self, *args, **kwargs):
        if not settings.DEBUG:
            # create fake users and notaries
            for i in range(5):
                user = UserProfile.objects.create(
                    first_name=fake.first_name_male(),
                    last_name=fake.last_name_male(),
                    email=fake.email(),
                    telephone=f'+38 066 666 66 66'
                )
                user.set_password('Zaqwerty123')
                user.save()
                EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
                Notary.objects.create(
                    first_name=fake.first_name_female(),
                    last_name=fake.last_name_female(),
                    email=fake.email(),
                    telephone=f'+38 066 666 66 66'
                )
            self.stdout.write("Init data successfully created")
        else:
            self.stdout.write("DEBUG is True! Init data not created.")
