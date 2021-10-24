"""
Events - Event Category model
"""
from django.db import models

from helpers.models import UUIDPrimaryKeyModel


class EventCategory(UUIDPrimaryKeyModel):
    name = models.CharField(max_length=150, unique=True, db_index=True)

    class Meta:
        verbose_name_plural = "Event categories"

    def __str__(self):
        return self.name
