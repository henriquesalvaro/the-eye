"""
API V1: Test - User routes
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


class UserTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "testuser"
        cls.user = User.objects.create(
            username="testuser",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
        )
        cls.user.set_password(cls.password)
        cls.user.save()
        Token.objects.create(user=cls.user)
        cls.user2 = User.objects.create(
            username="testuser2",
            email="testuser2@example.com",
            first_name="Test 2",
            last_name="User",
        )
        cls.user2.set_password(cls.password)
        cls.user2.save()
        Token.objects.create(user=cls.user2)

    def test_register_success(self):
        url = reverse("rest_register")
        payload = {
            "email": "user@test.com",
            "first_name": "User",
            "last_name": "Test",
            "password1": self.password,
            "password2": self.password,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="user@test.com")
        expected_payload = {
            "key": user.auth_token.key,
            "user": {
                "id": str(user.id),
                "email": payload.get("email"),
                "username": "user",
                "first_name": payload.get("first_name"),
                "last_name": payload.get("last_name"),
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
            },
        }
        self.assertDictEqual(
            response.json(), expected_payload, "Response payload matches expected"
        )

    def test_register_wrong_email(self):
        url = reverse("rest_register")
        payload = {
            "email": "usertest.com",
            "password1": self.password,
            "password2": self.password,
        }
        response = self.client.post(url, payload)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "Bad request for invalid email",
        )

    def test_register_missing_email(self):
        url = reverse("rest_register")
        payload = {
            "password1": self.password,
            "password2": self.password,
        }
        response = self.client.post(url, payload)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "Bad request for email missing",
        )

    def test_register_repeated_email(self):
        url = reverse("rest_register")
        payload = {
            "email": self.user.email,
            "password1": self.password,
            "password2": self.password,
        }
        response = self.client.post(url, payload)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "Bad request for existing email",
        )

    def test_register_different_passwords(self):
        url = reverse("rest_register")
        payload = {
            "email": "user@test.com",
            "password1": self.password,
            "password2": f"{self.password}1",
        }
        response = self.client.post(url, payload)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "Bad request for mismatch in passwords",
        )

    def test_register_missing_password(self):
        url = reverse("rest_register")
        payload = {
            "email": "user@test.com",
            "password1": self.password,
        }
        response = self.client.post(url, payload)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "Bad request for one password missing",
        )

    def test_login_success(self):
        url = reverse("rest_login")
        payload = {
            "email": self.user.email,
            "password": self.password,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_payload = {
            "key": self.user.auth_token.key,
            "user": {
                "id": str(self.user.id),
                "email": self.user.email,
                "username": self.user.username,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "is_active": self.user.is_active,
                "is_staff": self.user.is_staff,
                "is_superuser": self.user.is_superuser,
            },
        }
        self.assertDictEqual(
            response.json(), expected_payload, "Response payload matches expected"
        )

    def test_login_wrong_email(self):
        url = reverse("rest_login")
        payload = {
            "email": f"{self.user.email}.us",
            "password": self.password,
        }
        response = self.client.post(url, payload)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "Bad request for wrong email on sign in",
        )

    def test_login_wrong_password(self):
        url = reverse("rest_login")
        payload = {
            "email": self.user.email,
            "password": f"{self.password}1",
        }
        response = self.client.post(url, payload)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "Bad request for invalid password on sign in",
        )

    def test_update_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        url = reverse("rest_user_details")
        payload = {
            "first_name": "test",
            "last_name": "user",
        }
        response = self.client.patch(url, payload)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, "Successful patch user request"
        )

        data = response.json()
        self.assertEqual(
            data.get("first_name"), payload.get("first_name"), "New first_name matches"
        )
        self.assertEqual(
            data.get("last_name"), payload.get("last_name"), "New last_name matches"
        )

    def test_change_password_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        url = reverse("rest_password_change")
        new_password = "macarena95"
        payload = {
            "old_password": self.password,
            "new_password1": new_password,
            "new_password2": new_password,
        }
        response = self.client.post(url, payload)
        self.user.refresh_from_db()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Successful change password request",
        )
        self.assertTrue(
            self.user.check_password(new_password), "New password matches expected"
        )

    def test_change_password_fails_mismatch_password(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        url = reverse("rest_password_change")
        new_password = "macarena"
        payload = {
            "old_password": self.password,
            "new_password1": new_password,
            "new_password2": new_password + "a",
        }
        response = self.client.post(url, payload)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "Bad request when new passwords don't match",
        )

    def test_change_password_fails_wrong_old_password(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        url = reverse("rest_password_change")
        new_password = "macarena"
        payload = {
            "old_password": self.password + "a",
            "new_password1": new_password,
            "new_password2": new_password,
        }
        response = self.client.post(url, payload)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "Bad request when old passwords doesn't match",
        )

    def test_change_password_fails_missing_password_field(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        url = reverse("rest_password_change")
        new_password = "macarena"
        payload = {
            "old_password": self.password + "a",
            "new_password1": new_password,
        }
        response = self.client.post(url, payload)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "Bad request when a new password field is missing",
        )
