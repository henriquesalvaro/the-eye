"""
Events - Event Payload model
"""
from django.core.exceptions import ValidationError
from django.db import models
from jsonschema import Draft202012Validator, SchemaError

from helpers.models import UUIDPrimaryKeyModel


class EventPayload(UUIDPrimaryKeyModel):
    applications = models.ManyToManyField(
        "applications.Application",
        through="events.ApplicationEventPayload",
        related_name="event_payloads",
    )
    category = models.ForeignKey(
        "events.EventCategory", on_delete=models.CASCADE, related_name="event_payloads"
    )
    name = models.ForeignKey(
        "events.EventName", on_delete=models.CASCADE, related_name="event_payloads"
    )
    schema = models.JSONField(default=dict)

    class InvalidSchema(BaseException):
        pass

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.schema:
            raise ValueError(
                "An EventPayload requires a proper json schema definition."
            )
        try:
            Draft202012Validator.check_schema(self.schema)
        except SchemaError as exc:
            raise EventPayload.InvalidSchema(
                f"An EventPayload schema must be a valid JSON Schema. Error: {exc}"
            )

        return super().save(force_insert, force_update, using, update_fields)


class ApplicationEventPayload(UUIDPrimaryKeyModel):
    application = models.ForeignKey(
        "applications.Application",
        on_delete=models.CASCADE,
        related_name="event_payload_relations",
    )
    event_payload = models.ForeignKey(
        "events.EventPayload",
        on_delete=models.CASCADE,
        related_name="application_relations",
    )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        has_payload_with_category_and_name = EventPayload.objects.filter(
            applications=self.application,
            category=self.event_payload.category,
            name=self.event_payload.name,
        ).exists()
        if has_payload_with_category_and_name:
            raise ValueError(
                f"Application {self.application} already has an EventPayload defined for "
                f"Category {self.event_payload.category} and Name {self.event_payload.name}"
            )
        return super().save(force_insert, force_update, using, update_fields)

    def clean(self):
        has_payload_with_category_and_name = EventPayload.objects.filter(
            applications=self.application,
            category=self.event_payload.category,
            name=self.event_payload.name,
        ).exists()
        if has_payload_with_category_and_name:
            raise ValidationError(
                f"Application {self.application} already has an EventPayload defined for "
                f"Category {self.event_payload.category} and Name {self.event_payload.name}"
            )
