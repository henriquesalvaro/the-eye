"""
Accounts - User Model
"""
from django.contrib.auth.models import AbstractUser
from django.db import models

from helpers.models import UUIDPrimaryKeyModel


class User(AbstractUser, UUIDPrimaryKeyModel):
    email = models.EmailField(unique=True)
