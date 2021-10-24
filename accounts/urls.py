"""
Accounts - URL Configuration
"""
from django.urls import re_path, include


urlpatterns = [
    re_path(r"^api/v1/", include("accounts.api.v1.urls")),
]
