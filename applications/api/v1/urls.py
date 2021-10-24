"""
Applications - API V1 URLs
"""

from django.conf.urls import url, include
from rest_framework_nested import routers

from applications.api.v1.views import CurrentApplicationViewSet


router = routers.SimpleRouter()
router.register(
    r"application", CurrentApplicationViewSet, basename="current_application"
)


urlpatterns = [
    url(r"^", include(router.urls)),
]
