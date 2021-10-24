"""
Applications - API V1 + Middleware test
"""
from unittest import mock

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from applications.models import Application, ApplicationKey


def mock_response(*args, **kwargs):
    return Response(status=status.HTTP_204_NO_CONTENT)


class ApplicationKeyMiddlewareTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.application = Application.objects.create(name="The Eye")
        cls.application_key = ApplicationKey.objects.create(application=cls.application)
        cls.revoked_application_key = ApplicationKey.objects.create(
            application=cls.application, revoked=True
        )

    @mock.patch(
        "applications.api.v1.views.current_application.CurrentApplicationViewSet.list",
        side_effect=mock_response,
    )
    def test_valid_app_key_adds_application_to_request(self, mock_request):
        self.client.credentials(HTTP_APPLICATION_KEY=self.application_key.key)
        url = reverse("current_application-list")
        _ = self.client.get(url)
        self.assertEqual(
            mock_request.call_args[0][0].application.id,
            self.application_key.application.id,
            "Application matches expected requesting one",
        )

    def test_revoked_app_key_adds_no_application_to_request(self):
        self.client.credentials(HTTP_APPLICATION_KEY=self.revoked_application_key.key)
        url = reverse("current_application-list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            "Current application gets denied when using revoked key",
        )

    def test_invalid_app_key_adds_no_application_to_request(self):
        self.client.credentials(HTTP_APPLICATION_KEY="random key")
        url = reverse("current_application-list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            "Current application gets denied when using invalid key",
        )
