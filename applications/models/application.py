"""
Applications - Application model
"""
from django.db import models

from helpers.models import UUIDPrimaryKeyModel


class Application(UUIDPrimaryKeyModel):
    name = models.CharField(max_length=150, unique=True, db_index=True)

    def __str__(self):
        return self.name
