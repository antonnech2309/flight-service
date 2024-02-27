from datetime import timedelta
from unittest.mock import patch

from django.utils import timezone

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from airport.models import Order
from airport.serializers import OrderListSerializer, OrderDetailSerializer

ORDER_URL = reverse("airport:order-list")


class UnauthenticatedOrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ORDER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedOrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@test.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.order = Order.objects.create(user=self.user)

    def test_orders_list(self):
        Order.objects.create(user=self.user)

        res = self.client.get(ORDER_URL)

        orders = Order.objects.all()
        serializer = OrderListSerializer(orders, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_orders_by_created_at(self):
        original_now = timezone.now()

        custom_created_at = original_now - timedelta(days=5)

        with patch.object(timezone, "now", return_value=custom_created_at):
            order2 = Order.objects.create(user=self.user)

        res = self.client.get(
            ORDER_URL,
            {"created_at": custom_created_at.strftime('%Y-%m-%d')}
        )

        serializer1 = OrderListSerializer(self.order)
        serializer2 = OrderListSerializer(order2)

        self.assertNotIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res.data["results"])

    def test_retrieve_order(self):
        url = reverse("airport:order-detail", args=[self.order.id])
        res = self.client.get(url)
        serializer = OrderDetailSerializer(self.order)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
