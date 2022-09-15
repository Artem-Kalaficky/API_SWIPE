import pytest
from django.urls import reverse
from model_bakery import baker

from users.models import UserProfile

pytestmark = pytest.mark.django_db


class TestRegisterEndpoints:
    endpoint = reverse('register')

    def test_register(self, api_client):
        user = baker.prepare(UserProfile)
        expected_json = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'password1': 'Zaqwerty123',
            'password2': 'Zaqwerty123',
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 201
