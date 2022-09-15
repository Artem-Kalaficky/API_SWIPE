from django.urls import reverse
from model_bakery import baker
import json
import pytest

from users.models import Notary

pytestmark = pytest.mark.django_db


class TestNotaryEndpoints:
    endpoint = '/notaries/'

    def test_list(self, api_client, user):
        client = api_client()
        client.force_authenticate(user=user)
        baker.make(Notary, _quantity=3)

        response = client.get(
            reverse('notary-list')
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_create(self, api_client, admin_user):
        client = api_client()
        client.force_authenticate(user=admin_user)
        notary = baker.prepare(Notary)
        expected_json = {
            'first_name': notary.first_name,
            'last_name': notary.last_name,
            'email': notary.email,
        }

        response = client.post(
            reverse('notary-list'),
            data=expected_json,
            format='multipart'
        )

        assert response.status_code == 201

    def test_retrieve(self, api_client, user):
        client = api_client()
        client.force_authenticate(user=user)
        notary = baker.make(Notary)
        expected_json = {
            'id': notary.id,
            'first_name': notary.first_name,
            'last_name': notary.last_name,
            'email': notary.email,
            'telephone': notary.telephone,
            'avatar': notary.avatar
        }

        response = client.get(reverse('notary-detail', kwargs={'pk': notary.id}))

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_update(self, api_client, admin_user):
        client = api_client()
        client.force_authenticate(user=admin_user)
        old_notary = baker.make(Notary)
        new_notary = baker.prepare(Notary)
        currency_dict = {
            'first_name': new_notary.first_name,
            'last_name': new_notary.last_name,
            'email': new_notary.email
        }

        response = client.put(
            reverse('notary-detail', kwargs={'pk': old_notary.id}),
            currency_dict,
            format='multipart'
        )

        assert response.status_code == 200

    def test_delete(self, api_client, admin_user):
        client = api_client()
        client.force_authenticate(user=admin_user)
        notary = baker.make(Notary)

        response = client.delete(reverse('notary-detail', kwargs={'pk': notary.id}),)

        assert response.status_code == 204
        assert Notary.objects.all().count() == 0

