"""
Events admin
"""
from django.contrib import admin
from django.db.models import Prefetch

from events.models import Event, EventCategory, EventName, EventPayload, Session
from helpers.admin import JSONWidgetModelAdmin


class EventInline(admin.TabularInline):
    model = Event
    fields = ("category", "name", "data", "timestamp")
    readonly_fields = fields
    extra = 0

    def get_queryset(self, request):
        if getattr(self, "obj", False):
            return self.obj.events.all()
        return super().get_queryset(request)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        setattr(self, "obj", obj)
        return formset


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    model = EventCategory
    list_display = ("id", "name")


@admin.register(EventName)
class EventNameAdmin(admin.ModelAdmin):
    model = EventName
    list_display = ("id", "name")


@admin.register(EventPayload)
class EventPayloadAdmin(JSONWidgetModelAdmin):
    model = EventPayload
    list_display = ("id", "application", "category", "name")
    list_select_related = ["application", "category", "name"]


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    model = Session
    list_display = ("id", "application", "application_session_id", "created")
    inlines = [EventInline]
    list_select_related = ["application"]
    list_filter = ["application__name"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.resolver_match.url_name == "events_session_change":
            prefetch_events = Prefetch(
                "events",
                Event.objects.order_by("timestamp").select_related("category", "name"),
            )
            queryset = queryset.prefetch_related(prefetch_events)
        return queryset


@admin.register(Event)
class EventAdmin(JSONWidgetModelAdmin):
    model = Event
    list_display = ("id", "application", "category", "name", "timestamp")
    list_select_related = ["application", "category", "name"]
    list_filter = ["application__name", "category__name", "name__name"]

    def has_change_permission(self, request, obj=None):
        return False
