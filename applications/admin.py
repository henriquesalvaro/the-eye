"""
Applications admin
"""
from django.contrib import admin

from applications.models import ApplicationKey, Application


class ApplicationKeyInline(admin.TabularInline):
    model = ApplicationKey
    fields = ("id", "key", "revoked")
    readonly_fields = ("id", "key")
    extra = 0


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    inlines = [ApplicationKeyInline]
