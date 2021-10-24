"""
Django Admin helpers
"""
from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget


class JSONWidgetModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }
