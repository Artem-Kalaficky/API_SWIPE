from users.models import Apartment


def create_apartment(instance):
    Apartment.objects.create(ad=instance)