"""
Middleware Helpers
"""
from django.utils.deprecation import MiddlewareMixin

from applications.models import ApplicationKey


class ApplicationKeyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        key = request.META.get("HTTP_APPLICATION_KEY", "")
        request.application = None
        if key:
            try:
                application_key = ApplicationKey.objects.select_related(
                    "application"
                ).get(key=key, revoked=False)
                request.application = application_key.application
            except ApplicationKey.DoesNotExist:
                pass
