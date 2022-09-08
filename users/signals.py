from django.db.models.signals import post_save
from django.dispatch import receiver

from houses.services.creating_house import create_house
from users.models import UserProfile






