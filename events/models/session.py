"""
Events - Session model
"""
from django.db import models
from django.db.models.constraints import UniqueConstraint

from helpers.models import UUIDPrimaryKeyModel


class Session(UUIDPrimaryKeyModel):
    application = models.ForeignKey(
        "applications.Application",
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    application_session_id = models.UUIDField(db_index=True)
    created = models.DateTimeField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["application", "application_session_id"],
                name="unique_session_id_per_application",
            )
        ]
