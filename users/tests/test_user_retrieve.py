import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestUserRetrieveEndpoints:
    endpoint = reverse('profile-my-profile')

    def test_retrieve(self, api_client, user):
        client = api_client()
        client.force_authenticate(user=user)

        response = client.get(self.endpoint)

        assert response.status_code == 200
