from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from airport.tests.samples import sample_airplane_type

AIRPLANE_TYPE_URL = reverse("airport:airplanetype-list")


def detail_url(id: int):
    return f"/api/airport/airplane_types/{id}"


class AuthenticatedAirplaneTypeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@test.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.airplane_type = sample_airplane_type()

    def test_admin_required(self):
        res = self.client.get(AIRPLANE_TYPE_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneTypeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.airplane_type = sample_airplane_type()

    def test_delete_airplane_type(self):
        """If we have 404 error that indicates that
            we don`t have any of detail actions"""
        url = detail_url(self.airplane_type.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
