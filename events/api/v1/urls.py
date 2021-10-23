"""
Events - API V1 URLs
"""

from django.conf.urls import url, include
from rest_framework_nested import routers


router = routers.SimpleRouter()


urlpatterns = [
    url(r"^", include(router.urls)),
]
