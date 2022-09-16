from django.urls import reverse
from model_bakery import baker
import json
import pytest

from users.models import Ad

pytestmark = pytest.mark.django_db


class TestAdListEndpoints:
    endpoint = reverse('my-ad-list')

    def test_list(self, api_client, user):
        client = api_client()
        client.force_authenticate(user=user)
        baker.make(Ad, user=user, _quantity=3)

        response = client.get(
            self.endpoint
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3
