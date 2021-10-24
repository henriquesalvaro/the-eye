"""
Events - API V1 URLs
"""

from django.conf.urls import url, include
from rest_framework_nested import routers

from events.api.v1.views import (
    CreateEventViewSet,
    QueryEventsViewSet,
)

router = routers.SimpleRouter()
router.register(r"events", CreateEventViewSet, basename="create_event")
router.register(r"query-events", QueryEventsViewSet, basename="query_events")


urlpatterns = [
    url(r"^", include(router.urls)),
]
