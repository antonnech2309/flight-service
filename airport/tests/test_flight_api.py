from datetime import timedelta

from django.utils import timezone

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from airport.models import Flight
from airport.serializers import FlightListSerializer, FlightDetailSerializer
from airport.tests.samples import (
    sample_flight,
    sample_route,
    sample_airport,
    sample_airplane,
    sample_crew
)

FLIGHT_URL = reverse("airport:flight-list")


class UnauthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(FLIGHT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@test.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.flight = sample_flight()

    def test_flights_list(self):
        sample_flight()

        res = self.client.get(FLIGHT_URL)

        flights = Flight.objects.all()
        serializer = FlightListSerializer(flights, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for flight in res.data["results"]:
            flight.pop("tickets_available")
            self.assertIn(flight, serializer.data)

    def test_filter_flight_by_source(self):
        source = sample_airport(name="Zhylyanu")
        destination = sample_airport()
        route2 = sample_route(source=source, destination=destination)
        flight2 = sample_flight(route=route2)

        res_list = self.client.get(FLIGHT_URL)

        res_filter = self.client.get(
            FLIGHT_URL,
            {"source": f"{route2.source.name}"}
        )

        for res in res_list.data["results"]:
            if res["id"] == flight2.id:
                self.assertIn(res, res_filter.data["results"])
            if res["id"] == self.flight.id:
                self.assertNotIn(res, res_filter.data["results"])

    def test_filter_flight_by_destination(self):
        source = sample_airport(name="Zhylyanu")
        destination = sample_airport()
        route2 = sample_route(source=source, destination=destination)
        flight2 = sample_flight(route=route2)

        res_list = self.client.get(FLIGHT_URL)

        res_filter = self.client.get(
            FLIGHT_URL,
            {"destination": f"{route2.destination.name}"}
        )

        for res in res_list.data["results"]:
            if res["id"] == flight2.id:
                self.assertIn(res, res_filter.data["results"])
            if res["id"] == self.flight.id:
                self.assertNotIn(res, res_filter.data["results"])

    def test_filter_flights_by_departure_date(self):
        source = sample_airport(name="Zhylyanu")
        destination = sample_airport()
        route2 = sample_route(source=source, destination=destination)
        flight2 = sample_flight(
            route=route2,
            departure_time=timezone.now() + timedelta(days=5)
        )

        res_list = self.client.get(FLIGHT_URL)

        res_filter = self.client.get(
            FLIGHT_URL,
            {
                "departure_date": flight2.departure_time.strftime('%Y-%m-%d')
            }
        )

        for res in res_list.data["results"]:
            if res["id"] == flight2.id:
                self.assertIn(res, res_filter.data["results"])
            if res["id"] == self.flight.id:
                self.assertNotIn(res, res_filter.data["results"])

    def test_flight_create_forbidden(self):
        route = sample_route()
        airplane = sample_airplane()
        crew = sample_crew()
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": timezone.now() + timedelta(days=5),
            "arrival_time": timezone.now() + timedelta(days=5, hours=2),
            "crew": [crew.id]
        }

        res = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_using_detail_serializer(self):
        url = reverse("airport:flight-detail", args=[self.flight.id])
        res = self.client.get(url)

        flight = Flight.objects.get(id=self.flight.id)
        serializer = FlightDetailSerializer(flight)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res.data.pop("tickets_available")
        self.assertEqual(res.data, serializer.data)


class AdminCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.flight = sample_flight()

    def test_create_flight(self):
        route = sample_route()
        airplane = sample_airplane()
        crew = sample_crew()
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": timezone.now() + timedelta(days=5),
            "arrival_time": timezone.now() + timedelta(days=5, hours=2),
            "crew": [crew.id]
        }

        res = self.client.post(FLIGHT_URL, payload)
        res_list = self.client.get(FLIGHT_URL)

        flight = Flight.objects.get(id=res.data["id"])
        serializer = FlightListSerializer(flight)
        print(res.data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for res in res_list.data["results"]:
            if res["id"] == flight.id:
                res.pop("tickets_available")
                self.assertEqual(res, serializer.data)
