"""
Events - Create Event tests
"""
from unittest import mock
import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from applications.models import Application, ApplicationKey


class CreateEventTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.application = Application.objects.create(name="The Eye")
        cls.application_key = ApplicationKey.objects.create(application=cls.application)

    class MockAsyncTask:
        def __init__(self, *args, **kwargs):
            self.id = uuid.uuid4()

    @mock.patch(
        "events.api.v1.views.create_event.process_event.delay",
        side_effect=MockAsyncTask,
    )
    def test_event_from_proper_application_gets_sent_to_queue(self, mock_process_event):
        self.client.credentials(HTTP_APPLICATION_KEY=self.application_key.key)
        url = reverse("create_event-list")
        response = self.client.post(url, {})
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        mock_process_event.assert_called_once()

    @mock.patch(
        "events.api.v1.views.create_event.process_event.delay",
        side_effect=MockAsyncTask,
    )
    def test_event_with_invalid_application_key_gets_denied(self, mock_process_event):
        self.client.credentials(HTTP_APPLICATION_KEY="macarena")
        url = reverse("create_event-list")
        response = self.client.post(url, {})
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        mock_process_event.not_called()
