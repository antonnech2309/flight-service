from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from airport.serializers import RouteListSerializer
from airport.tests.samples import sample_route, sample_airport

ROUTE_URL = reverse("airport:route-list")


def detail_url(id: int):
    return f"/api/airport/routes/{id}"


class AuthenticatedRouteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@test.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.route = sample_route()

    def test_admin_required(self):
        res = self.client.get(ROUTE_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminRouteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.route = sample_route()

    def test_filter_route_by_source(self):
        source = sample_airport(name="Zhylyanu")
        destination = sample_airport()
        route2 = sample_route(source=source, destination=destination)

        res = self.client.get(
            ROUTE_URL,
            {"source": f"{route2.source.name}"}
        )

        serializer1 = RouteListSerializer(self.route)
        serializer2 = RouteListSerializer(route2)

        self.assertNotIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res.data["results"])

    def test_filter_route_by_destination(self):
        source = sample_airport(name="Zhylyanu")
        destination = sample_airport()
        route2 = sample_route(source=source, destination=destination)

        res = self.client.get(
            ROUTE_URL,
            {"destination": f"{route2.destination.name}"}
        )

        serializer1 = RouteListSerializer(self.route)
        serializer2 = RouteListSerializer(route2)

        self.assertNotIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res.data["results"])

    def test_delete_route(self):
        """If we have 404 error that indicates that
            we don`t have any of detail actions"""
        url = detail_url(self.route.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
