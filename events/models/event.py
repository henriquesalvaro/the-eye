"""
Events - Event model
"""
from django.db import models
from jsonschema import validate, ValidationError

from events.models.event_payload import EventPayload
from helpers.models import UUIDPrimaryKeyModel


class Event(UUIDPrimaryKeyModel):
    session = models.ForeignKey(
        "events.Session",
        on_delete=models.CASCADE,
        related_name="events",
    )
    # Controlled redundancy (FK is indexed - "quicker" access to events from Applications)
    application = models.ForeignKey(
        "applications.Application",
        on_delete=models.CASCADE,
        related_name="events",
    )
    category = models.ForeignKey(
        "events.EventCategory", on_delete=models.CASCADE, related_name="events"
    )
    name = models.ForeignKey(
        "events.EventName", on_delete=models.CASCADE, related_name="events"
    )
    data = models.JSONField(default=dict)
    timestamp = models.DateTimeField(db_index=True)
    received = models.DateTimeField()
    processed = models.DateTimeField()

    class InvalidPayload(BaseException):
        pass

    class NoPayloadDefinition(BaseException):
        pass

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        try:
            event_payload = EventPayload.objects.get(
                category=self.category,
                name=self.name,
                applications=self.application,
            )
        except EventPayload.DoesNotExist:
            raise Event.NoPayloadDefinition(
                f"There's no payload definition for this event. Category: {self.category}. "
                f"Name: {self.name}. Application: {self.application}."
            )

        try:
            validate(self.data, event_payload.schema)
        except ValidationError as exc:
            raise Event.InvalidPayload(f"Invalid event payload. Error: {exc}")

        return super().save(force_insert, force_update, using, update_fields)
