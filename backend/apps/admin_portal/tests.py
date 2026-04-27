from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import Role, User, UserProfile

class AdminPortalAPITest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='platform-admin@example.com',
            email='platform-admin@example.com',
            password='SecurePass123!',
            role=Role.PLATFORM_ADMIN,
        )
        UserProfile.objects.create(user=self.admin_user, full_name='Platform Admin', email=self.admin_user.email)

        self.applicant_user = User.objects.create_user(
            username='applicant@example.com',
            email='applicant@example.com',
            password='SecurePass123!',
            role=Role.APPLICANT,
        )
        UserProfile.objects.create(user=self.applicant_user, full_name='Applicant User', email=self.applicant_user.email)

    def test_admin_can_get_overview(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get(reverse('admin_portal-overview'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_users', response.data)
        self.assertIn('role_breakdown', response.data)

    def test_non_admin_is_forbidden(self):
        self.client.force_authenticate(user=self.applicant_user)

        response = self.client.get(reverse('admin_portal-users'))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_and_create_users(self):
        self.client.force_authenticate(user=self.admin_user)

        list_response = self.client.get(reverse('admin_portal-users'))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(list_response.data['count'], 2)

        payload = {
            'full_name': 'Support Team Member',
            'email': 'support@example.com',
            'role': Role.SUPPORT_STAFF,
            'password': 'ComplexPass123!',
        }
        create_response = self.client.post(reverse('admin_portal-users'), payload, format='json')

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_response.data['email'], payload['email'])
        self.assertEqual(create_response.data['role'], payload['role'])
        self.assertTrue(User.objects.filter(email=payload['email']).exists())