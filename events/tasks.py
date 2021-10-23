"""
Events - Process events
"""
from logging import getLogger

from celery import shared_task

from events.api.v1.serializers import CreateEventSerializer
from events.models import Event

logger = getLogger("amazon-logs")


def _error(label: str, event_payload: dict, **kwargs) -> dict:
    message = {"error": label, "payload": event_payload, **kwargs}
    logger.error(message, exc_info=True)
    return message


@shared_task
def process_event(event_payload: dict) -> dict:

    serializer = CreateEventSerializer(data=event_payload)
    if not serializer.is_valid(raise_exception=False):
        message = _error(
            "fail_to_parse_event", event_payload, details=serializer.errors
        )
        return message

    try:
        event = serializer.save()
    except (Event.NoPayloadDefinition, Event.InvalidPayload) as exc:
        message = _error("fail_to_create_event", event_payload, details=str(exc))
        return message

    return {"event_created": str(event.id)}
