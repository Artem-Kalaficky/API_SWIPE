from django.urls import reverse
from model_bakery import baker
import pytest

from users.models import UserProfile

pytestmark = pytest.mark.django_db


class TestUserUpdateEndpoints:

    def test_update_my_contacts(self, api_client, user):
        client = api_client()
        client.force_authenticate(user=user)
        baker.make(UserProfile)
        new_user = baker.prepare(UserProfile)
        currency_dict = {
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'telephone': new_user.telephone
        }

        response = client.put(
            reverse('profile-change-my-contacts'),
            currency_dict,
            format='json'
        )

        assert response.status_code == 200
