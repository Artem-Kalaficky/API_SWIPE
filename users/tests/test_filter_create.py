import pytest
from django.urls import reverse
from model_bakery import baker

from users.models import Filter

pytestmark = pytest.mark.django_db


class TestFilterCreateEndpoints:
    endpoint = reverse('my-filter-list')

    def test_create(self, api_client, user):
        client = api_client()
        client.force_authenticate(user=user)
        my_filter = baker.prepare(Filter)
        expected_json = {
            'first_name': my_filter.type,
            'number_of_rooms': my_filter.number_of_rooms
        }

        response = client.post(
            self.endpoint,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 201
