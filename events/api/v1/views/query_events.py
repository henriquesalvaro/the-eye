"""
Events - API V1 Query Events Views
"""
from django_filters import rest_framework as filters
from rest_framework import (
    viewsets,
    permissions,
)

from events.api.v1.serializers import QueryEventSerializer
from events.models import Event


class EventFilterSet(filters.FilterSet):
    session_id = filters.UUIDFilter(field_name="session__application_session_id")
    start = filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    end = filters.DateTimeFilter(field_name="timestamp", lookup_expr="lte")
    category = filters.CharFilter(field_name="category__name")
    name = filters.CharFilter(field_name="name__name")

    class Meta:
        model = Event
        fields = ("application_id", "timestamp")


class QueryEventsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.order_by("timestamp")
    permission_classes = [permissions.IsAdminUser]
    serializer_class = QueryEventSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EventFilterSet

    def get_queryset(self):
        return Event.objects.select_related("session", "category", "name").order_by(
            "timestamp"
        )
