from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from airport.serializers import CrewSerializer
from airport.tests.samples import sample_crew

CREW_URL = reverse("airport:crew-list")


def detail_url(id: int):
    return f"/api/airport/crews/{id}"


class AuthenticatedCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@test.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.crew = sample_crew()

    def test_admin_required(self):
        res = self.client.get(CREW_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.crew = sample_crew()

    def test_filter_crew_by_first_name(self):
        crew2 = sample_crew(first_name="test_first", last_name="test_last")

        res = self.client.get(
            CREW_URL,
            {"first_name": f"{crew2.first_name}"}
        )

        serializer1 = CrewSerializer(self.crew)
        serializer2 = CrewSerializer(crew2)

        self.assertNotIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res.data["results"])

    def test_filter_crew_by_last_name(self):
        crew2 = sample_crew(first_name="test_first", last_name="test_last")

        res = self.client.get(
            CREW_URL,
            {"last_name": f"{crew2.last_name}"}
        )

        serializer1 = CrewSerializer(self.crew)
        serializer2 = CrewSerializer(crew2)

        self.assertNotIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res.data["results"])

    def test_delete_crew(self):
        """If we have 404 error that indicates that
            we don`t have any of detail actions"""
        url = detail_url(self.crew.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
