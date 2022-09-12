from django.db.models.signals import post_save
from django.dispatch import receiver

from houses.services.creating_house import create_house, create_advantage
from users.models import UserProfile, House


@receiver(post_save, sender=UserProfile)
def post_save_user_is_developer(created, **kwargs):
    instance = kwargs.get('instance')
    if created and instance.is_developer:
        create_house(instance)


@receiver(post_save, sender=House)
def post_save_user_is_developer(created, **kwargs):
    instance = kwargs.get('instance')
    if created:
        create_advantage(instance)
