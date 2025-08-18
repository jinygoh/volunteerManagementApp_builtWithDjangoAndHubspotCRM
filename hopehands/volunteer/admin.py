"""
Configuration for the Django admin interface for the volunteer app.

This file is used to register the Volunteer model with the Django admin,
allowing administrators to view, add, edit, and delete volunteer records
through the built-in admin dashboard.
"""
from django.contrib import admin
from .models import Volunteer

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    """
    Customizes the display and behavior of the Volunteer model in the Django admin.
    """
    list_display = ('first_name', 'last_name', 'email', 'status', 'hubspot_id')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('status', 'preferred_volunteer_role')
    readonly_fields = ('hubspot_id',)
