"""
Applications - API V1 Current Application view
"""
from rest_framework import viewsets, status
from rest_framework.response import Response

from applications.api.v1.serializers import ApplicationSerializer
from helpers.permissions import IsApplication


class CurrentApplicationViewSet(viewsets.ViewSet):
    permission_classes = [IsApplication]

    def list(self, request, *args, **kwargs):
        return Response(
            ApplicationSerializer(request.application).data,
            status=status.HTTP_200_OK,
        )
