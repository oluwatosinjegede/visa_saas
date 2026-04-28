from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Payment, Subscription


class PaymentFlowTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="payment_user",
            email="payment_user@example.com",
            password="StrongPass123",
        )
        self.client.force_authenticate(self.user)

    def test_should_list_subscription_plans(self):
        response = self.client.get(reverse("payments-plans"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data.get("plans", [])), 3)

    def test_should_initialize_and_verify_payment_and_upgrade_subscription(self):
        initialize_response = self.client.post(
            reverse("payments-initialize"),
            {"plan": "PREMIUM", "provider": "paystack"},
            format="json",
        )
        self.assertEqual(initialize_response.status_code, status.HTTP_200_OK)
        self.assertIn("reference", initialize_response.data)

        verify_response = self.client.get(
            reverse("payments-verify"),
            {"reference": initialize_response.data["reference"]},
        )
        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)

        payment = Payment.objects.get(reference=initialize_response.data["reference"])
        self.assertEqual(payment.status, "success")

        subscription = Subscription.objects.get(user=self.user)
        self.assertEqual(subscription.plan, "PREMIUM")
        self.assertTrue(subscription.active)