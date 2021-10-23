"""
Events - EventPayload tests
"""
from django.test import TestCase

from applications.models import Application
from events.models import EventCategory, EventName, EventPayload


class EventPayloadTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = EventCategory.objects.create(name="Category")
        cls.name = EventName.objects.create(name="Name")

    def test_event_payload_with_valid_schema_gets_created(self):
        event_payload = EventPayload.objects.create(
            category=self.category,
            name=self.name,
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
        self.assertIsNotNone(event_payload)

    def test_event_payload_with_invalid_schema_fails_to_create(self):
        with self.assertRaises(EventPayload.InvalidSchema):
            EventPayload.objects.create(
                category=self.category, name=self.name, schema={"type": "nonexistent"}
            )

    def test_event_payload_with_no_schema_fails_to_create(self):
        with self.assertRaises(ValueError):
            EventPayload.objects.create(
                category=self.category,
                name=self.name,
            )
