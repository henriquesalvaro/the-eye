"""
Events - API V1 Query Event Serializers
"""
from rest_framework import serializers

from events.models import Event


class QueryEventSerializer(serializers.ModelSerializer):
    session_id = serializers.UUIDField(source="session.application_session_id")
    category = serializers.CharField(source="category.name")
    name = serializers.CharField(source="name.name")

    class Meta:
        model = Event
        fields = (
            "id",
            "application",
            "session_id",
            "category",
            "name",
            "data",
            "timestamp",
        )
