import json

import pytest
from allauth.account.models import EmailAddress
from django.urls import reverse
from model_bakery import baker

from users.models import UserProfile

pytestmark = pytest.mark.django_db


class TestLoginEndpoints:
    endpoint = reverse('login')

    def test_login(self, api_client):
        user = baker.make(UserProfile)
        user.set_password('Zaqwerty123')
        user.save()
        EmailAddress.objects.create(
            user=user,
            email=user.email,
            primary=True,
            verified=True
        )
        expected_json = {
            'email': user.email,
            'password': 'Zaqwerty123',
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 200
        assert 'access_token' in json.loads(response.content)
