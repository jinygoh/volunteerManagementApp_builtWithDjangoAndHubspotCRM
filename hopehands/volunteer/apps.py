"""
App configuration for the 'volunteer' Django app.

This file defines the configuration for the volunteer application,
including its name and the default type for auto-created primary key fields.
"""
from django.apps import AppConfig


class VolunteerConfig(AppConfig):
    """
    Configuration class for the 'volunteer' app.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "volunteer"
