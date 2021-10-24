"""
Applications - URL Configuration
"""
from django.conf.urls import url, include


urlpatterns = [url(r"^api/v1/", include("applications.api.v1.urls"))]
