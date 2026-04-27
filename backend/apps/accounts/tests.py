from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class AccountsAuthTests(APITestCase):
    @staticmethod
    def error_fields(response):
        return response.data.get("errors", {})

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
        user = get_user_model().objects.get(email="test@example.com")
        self.assertEqual(user.username, "test@example.com")

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

    def test_register_requires_email(self):
        response = self.client.post(
            reverse("accounts-register"),
            {"full_name": "No Email", "password": "StrongPass123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", self.error_fields(response))

    def test_register_requires_password(self):
        response = self.client.post(
            reverse("accounts-register"),
            {"full_name": "No Password", "email": "no-password@example.com"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", self.error_fields(response))

    def test_register_rejects_duplicate_email(self):
        payload = {
            "full_name": "First User",
            "email": "duplicate@example.com",
            "password": "StrongPass123",
        }
        first = self.client.post(reverse("accounts-register"), payload, format="json")
        second = self.client.post(
            reverse("accounts-register"),
            {**payload, "full_name": "Second User"},
            format="json",
        )

        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second.status_code, status.HTTP_400_BAD_REQUEST)
       self.assertIn("email", self.error_fields(second))

    def test_register_succeeds_without_username(self):
        response = self.client.post(
            reverse("accounts-register"),
            {
                "full_name": "No Username Needed",
                "email": "nousername@example.com",
                "password": "StrongPass123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_user = get_user_model().objects.get(email="nousername@example.com")
        self.assertEqual(created_user.username, "nousername@example.com")

    def test_login_does_not_require_username_field(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            username="existing@example.com",
            email="existing@example.com",
            password="StrongPass123",
        )

        response = self.client.post(
            reverse("accounts-login"),
            {
                "email": "existing@example.com",
                "password": "StrongPass123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("username", self.error_fields(response))
        self.assertIn("access", response.data)