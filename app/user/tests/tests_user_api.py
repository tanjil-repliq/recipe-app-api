"""
Tests for user api
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


from rest_framework import status
from rest_framework.test import APIClient


def create_user(**params):
    # Function to create a user
    return get_user_model().objects.create_user(**params)


CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


class PublicUserApiTests(TestCase):
    """Test all the public features of user api"""

    def setUp(self):
        self.client = APIClient()

    def test_user_create(self):
        """Test a successful user create request"""

        payload = {
            "email": "user@example.com",
            "password": "testpass123",
            "name": "Test User",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        """Test creating a user that already exists"""

        payload = {
            "email": "user@example.com",
            "password": "testpass123",
            "name": "Test User",
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password is more than 5 characters"""

        payload = {
            "email": "user@example.com",
            "password": "test",
            "name": "Test User",
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exist = get_user_model().objects.filter(email=payload["email"]).exists()

        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """Test token creation for a registered user"""

        user_details = {
            "email": "user@example.com",
            "password": "testpass123",
            "name": "Test User",
        }

        create_user(**user_details)
        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_token_creation_for_bad_user(self):
        """Test token creation for a non-existent user"""

        create_user(email="test@example.com", password="testpass123")
        payload = {"email": "test@example.com", "password": "testpass"}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_creation_with_blank_password(self):
        """Test token creation with a blank password"""

        create_user(email="test@example.com", password="testpass123")
        payload = {"email": "test@example.com", "password": ""}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
