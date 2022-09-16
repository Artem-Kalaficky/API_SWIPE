import pytest
from django.urls import reverse
from model_bakery import baker

from users.models import Ad

pytestmark = pytest.mark.django_db


class TestAdCreateEndpoints:
    endpoint = reverse('my-ad-list')

    def test_create(self, api_client, user):
        client = api_client()
        client.force_authenticate(user=user)
        ad = baker.prepare(Ad, purpose='cottage')
        expected_json = {
            'address': ad.address,
            'purpose': ad.purpose,
            'number_of_rooms': ad.number_of_rooms,
            'apartment_layout': ad.apartment_layout,
            'total_area': ad.total_area,
            'payment_option': ad.payment_option,
            'description': ad.description,
            'price': ad.price,
            'photos': []
        }

        response = client.post(
            self.endpoint,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 201
