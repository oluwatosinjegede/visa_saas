from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AccountsAuthTests(APITestCase):
    def test_register_login_and_profile(self):
        register_response = self.client.post(
            reverse("accounts-register"),
            {
                "full_name": "Test Applicant",
                "email": "test@example.com",
                "password": "StrongPass123",
            },
            format="json",
        )

        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", register_response.data)
        self.assertIn("refresh", register_response.data)
        self.assertEqual(register_response.data["user"]["email"], "test@example.com")

        login_response = self.client.post(
            reverse("accounts-login"),
            {"email": "test@example.com", "password": "StrongPass123"},
            format="json",
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)

        access_token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        profile_response = self.client.get(reverse("accounts-profile"))

        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data["email"], "test@example.com")
        self.assertEqual(profile_response.data["full_name"], "Test Applicant")