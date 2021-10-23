"""
Applications - Application Key model
"""
import binascii
import os

from django.db import models

from helpers.models import UUIDPrimaryKeyModel


class ApplicationKey(UUIDPrimaryKeyModel):
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
