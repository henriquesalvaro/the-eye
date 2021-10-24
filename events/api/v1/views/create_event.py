"""
Events - API V1 Create Event Views
"""
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.response import Response

from events.tasks import process_event
from helpers.permissions import IsApplication


class CreateEventViewSet(viewsets.GenericViewSet):
    permission_classes = [IsApplication]

    def create(self, request, *args, **kwargs):
        data = {
            "received": timezone.now(),
            "application": request.application.id,
            **request.data,
        }
        async_task = process_event.delay(data)
        return Response({"protocol": async_task.id}, status=status.HTTP_200_OK)
