from django.core.management import BaseCommand

from api_swipe import settings
from users.models import Notary


class Command(BaseCommand):
    help = 'Init data to raise the project'

    def handle(self, *args, **kwargs):
        if not settings.DEBUG:
            # create notaries
            for i in range(1, 6):
                Notary.objects.create(first_name=f'Name{i}',
                                      last_name=f'Surname{i}',
                                      email=f'test{i}@gmail.com',
                                      telephone=f'+38 066 666 66 66')
            self.stdout.write("Init data successfully created")
        else:
            self.stdout.write("DEBUG is True! Init data not created.")
