from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from airport.models import Airport
from airport.serializers import AirportSerializer
from airport.tests.samples import sample_airport

AIRPORT_URL = reverse("airport:airport-list")


class UnauthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AIRPORT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@test.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.airport = sample_airport()

    def test_airports_list(self):
        sample_airport()

        res = self.client.get(AIRPORT_URL)

        airports = Airport.objects.all()
        serializer = AirportSerializer(airports, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_airports_by_name(self):
        airport2 = sample_airport(name="Zhylyanu")

        res = self.client.get(AIRPORT_URL, {"name": f"{airport2.name}"})

        serializer1 = AirportSerializer(self.airport)
        serializer2 = AirportSerializer(airport2)

        self.assertNotIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res.data["results"])

    def test_create_airport_forbidden(self):
        payload = {
            "name": "Test",
            "closest_big_city": "Test_city"
        }

        res = self.client.post(AIRPORT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.airport = sample_airport()

    def test_create_airport(self):
        payload = {
            "name": "Test",
            "closest_big_city": "Test_city"
        }

        res = self.client.post(AIRPORT_URL, payload)

        airport = Airport.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(airport, key))
