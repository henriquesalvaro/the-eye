"""
Events - Event Payload model
"""
from django.db import models
from jsonschema import Draft202012Validator, SchemaError

from helpers.models import UUIDPrimaryKeyModel


class EventPayload(UUIDPrimaryKeyModel):
    application = models.ForeignKey(
        "applications.Application",
        on_delete=models.CASCADE,
        related_name="event_payloads",
    )
    category = models.ForeignKey(
        "events.EventCategory", on_delete=models.CASCADE, related_name="event_payloads"
    )
    name = models.ForeignKey(
        "events.EventName", on_delete=models.CASCADE, related_name="event_payloads"
    )
    schema = models.JSONField(default=dict)

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
            raise ValueError(
                f"An EventPayload schema must be a valid JSON Schema. Error: {exc}"
            )

        return super().save(force_insert, force_update, using, update_fields)
