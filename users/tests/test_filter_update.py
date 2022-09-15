from django.urls import reverse
from model_bakery import baker
import pytest

from users.models import Filter

pytestmark = pytest.mark.django_db


class TestFilterUpdateEndpoints:

    def test_update(self, api_client, user):
        client = api_client()
        client.force_authenticate(user=user)
        old_filter = baker.make(Filter, user=user, type='all')
        new_filter = baker.prepare(Filter)
        currency_dict = {
            'type': new_filter.type,
        }

        response = client.put(
            reverse('my-filter-detail', kwargs={'id': old_filter.id}),
            currency_dict,
            format='json'
        )

        assert response.status_code == 200
