"""
Events - Process Event tests
"""
import uuid

from django.test import TestCase
from django.utils import timezone

from applications.models import Application
from events.models import (
    Event,
    EventCategory,
    EventName,
    EventPayload,
    Session,
)
from events.tasks import process_event


class ProcessEventTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.application = Application.objects.create(name="The Eye")
        cls.session = Session.objects.create(
            application=cls.application,
            application_session_id=uuid.uuid4(),
            created=timezone.now(),
        )
        cls.category = EventCategory.objects.create(name="Category")
        cls.name = EventName.objects.create(name="Name")
        cls.name_2 = EventName.objects.create(name="Name 2")
        cls.event_payload = EventPayload.objects.create(
            category=cls.category,
            name=cls.name,
            schema={
                "type": "object",
                "required": [
                    "host",
                    "path",
                ],
                "properties": {"host": {"type": "string"}, "path": {"type": "string"}},
                "additionalProperties": False,
            },
        )
        cls.event_payload.applications.set([cls.application])

    def setUp(self) -> None:
        self.payload = {
            "application": self.application.id,
            "session_id": self.session.application_session_id,
            "category": self.category.name,
            "name": self.name.name,
            "data": {"host": "www.google.com", "path": "/"},
            "received": timezone.now().isoformat(),
            "timestamp": (timezone.now() - timezone.timedelta(minutes=1)).isoformat(),
        }

    def test_event_with_proper_payload_gets_processed(self):
        event_created = process_event.delay(self.payload)
        self.assertEqual(
            event_created.result.keys(), {"event_created"}, "Event was created properly"
        )
        event = Event.objects.filter(
            id=event_created.result.get("event_created")
        ).first()
        self.assertIsNotNone(event)

    def test_event_without_event_payload_fails_to_get_created(self):
        self.payload["name"] = self.name_2.name
        event_created = process_event.delay(self.payload)
        self.assertEqual(
            event_created.result.get("error"),
            "fail_to_create_event",
        )

    def test_event_with_invalid_payload_fails_to_get_created(self):
        self.payload["data"] = {"macarena": "macarena"}
        event_created = process_event.delay(self.payload)
        self.assertEqual(
            event_created.result.get("error"),
            "fail_to_create_event",
        )

    def test_event_with_future_timestamp_fails_to_get_parsed(self):
        self.payload["received"] = (
            timezone.now() - timezone.timedelta(hours=1)
        ).isoformat()
        event_created = process_event.delay(self.payload)
        self.assertEqual(
            event_created.result.get("error"),
            "fail_to_parse_event",
        )
