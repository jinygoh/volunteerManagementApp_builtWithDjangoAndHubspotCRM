# hopehands/volunteer/models.py

"""
This file defines the Django models for the volunteer application.
Models are the single, definitive source of information about your data.
They contain the essential fields and behaviors of the data you’re storing.
Django follows the DRY Principle. The goal is to define your data model in one
place and automatically derive things from it.

In this application, the Volunteer model is used to temporarily store volunteer
data before it is sent to HubSpot. It also serves as the basis for the
`VolunteerForm`.
"""

from django.db import models
from django.db.models import Q

class Volunteer(models.Model):
    """
    Represents a volunteer in the local database.
    This model's fields correspond to the fields in the volunteer signup form.
    The data is saved here before being sent to the HubSpot CRM.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    first_name = models.CharField(max_length=50, help_text="The volunteer's first name.")
    last_name = models.CharField(max_length=50, help_text="The volunteer's last name.")
    email = models.EmailField(unique=True, help_text="The volunteer's email address. Must be unique.")
    phone_number = models.CharField(max_length=15, help_text="The volunteer's phone number.")
    preferred_volunteer_role = models.CharField(max_length=100, help_text="The volunteer's preferred role.")
    availability = models.CharField(max_length=100, help_text="The volunteer's availability.")
    how_did_you_hear_about_us = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="How the volunteer heard about the organization. Optional."
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="The application status, used in the admin approval workflow."
    )
    hubspot_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Stores the HubSpot Contact ID after a volunteer is approved and synced."
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['hubspot_id'],
                condition=~models.Q(hubspot_id=None),
                name='unique_hubspot_id_when_not_null'
            )
        ]

    def __str__(self):
        """Returns the full name of the volunteer for display purposes."""
        return f"{self.first_name} {self.last_name}"
