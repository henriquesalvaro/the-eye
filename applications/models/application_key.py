"""
Applications - Application Key model
"""
import binascii
import os
import uuid

from django.db import models


class ApplicationKey(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    application = models.ForeignKey(
        "applications.Application", on_delete=models.CASCADE, related_name="keys"
    )
    key = models.CharField(max_length=40, unique=True, db_index=True)
    revoked = models.BooleanField(default=False)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.key:
            self.key = self.generate_key()
        return super().save(force_insert, force_update, using, update_fields)

    @staticmethod
    def generate_key():
        return binascii.hexlify(os.urandom(20)).decode()
