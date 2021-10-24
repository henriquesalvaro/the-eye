"""
Events - API V1 Create Event Serializers
"""
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from applications.models import Application
from events.models import (
    Event,
    EventCategory,
    EventName,
    Session,
)


class CreateEventSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    application = serializers.PrimaryKeyRelatedField(queryset=Application.objects.all())
    category = serializers.SlugRelatedField(
        queryset=EventCategory.objects.all(), slug_field="name"
    )
    name = serializers.SlugRelatedField(
        queryset=EventName.objects.all(), slug_field="name"
    )
    data = serializers.JSONField()
    timestamp = serializers.DateTimeField()
    received = serializers.DateTimeField()

    def validate(self, attrs):
        if attrs.get("timestamp") > attrs.get("received"):
            raise ValidationError(
                {"timestamp": "You can't create an event in the future."}
            )
        application_session_id = attrs.pop("session_id")
        attrs["session"], _ = Session.objects.get_or_create(
            application=attrs.get("application"),
            application_session_id=application_session_id,
            defaults={
                "created": timezone.now(),
            },
        )
        return attrs

    def save(self, **kwargs):
        return Event.objects.create(**self.validated_data, processed=timezone.now())
