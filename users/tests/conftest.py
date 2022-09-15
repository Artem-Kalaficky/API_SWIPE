import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from users.models import UserProfile, Filter


@pytest.fixture
def api_client():
    return APIClient


@pytest.fixture
def user():
    user = UserProfile.objects.create(
        first_name='Николай Карпов',
        last_name='Иванов',
        email='test@gmail.com'
    )
    user.set_password('Zaqwerty123')
    user.save()
    return user


@pytest.fixture
def developer_user():
    user = UserProfile.objects.create(
        first_name='Максим',
        last_name='Стройный',
        email='developer@gmail.com',
        is_developer=True
    )
    user.set_password('Zaqwerty123')
    user.save()
    return user






