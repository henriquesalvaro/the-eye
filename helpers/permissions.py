"""
Permissions helpers
"""
from rest_framework.permissions import BasePermission


class IsApplication(BasePermission):
    def has_permission(self, request, view):
        return request.application is not None
