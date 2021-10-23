"""
Events - Event model
"""
from django.db import models
from django.db.models.constraints import UniqueConstraint

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
