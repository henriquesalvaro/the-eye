"""
Events - Event tests
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


class EventTestCase(TestCase):
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

    def test_event_with_proper_data_and_payload_gets_created(self):
        event = Event.objects.create(
            application=self.application,
            session=self.session,
            category=self.category,
            name=self.name,
            data={"host": "www.google.com", "path": "/"},
            timestamp=timezone.now(),
            received=timezone.now(),
            processed=timezone.now(),
        )
        self.assertIsNotNone(event)

    def test_event_with_no_payload_definition_fails_to_create(self):
        with self.assertRaises(Event.NoPayloadDefinition):
            Event.objects.create(
                application=self.application,
                session=self.session,
                category=self.category,
                name=self.name_2,
                data={"host": "www.google.com", "path": "/"},
                timestamp=timezone.now(),
                received=timezone.now(),
                processed=timezone.now(),
            )

    def test_event_with_invalid_payload_fails_to_create(self):
        with self.assertRaises(Event.InvalidPayload):
            Event.objects.create(
                application=self.application,
                session=self.session,
                category=self.category,
                name=self.name,
                data={"host": "www.google.com", "macarena": "macarena"},
                timestamp=timezone.now(),
                received=timezone.now(),
                processed=timezone.now(),
            )
