"""
Applications - Application model
"""
import uuid

from django.db import models


class Application(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=150, unique=True, db_index=True)
