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

    # The volunteer's full name.
    name = models.CharField(max_length=100)
    # The volunteer's email address. This should be unique.
    email = models.EmailField(unique=True)
    # The volunteer's phone number.
    phone_number = models.CharField(max_length=15)
    # The volunteer's preferred role.
    preferred_volunteer_role = models.CharField(max_length=100)
    # The volunteer's availability.
    availability = models.CharField(max_length=100)
    # How the volunteer heard about the organization. This field is optional.
    how_did_you_hear_about_us = models.CharField(max_length=200, blank=True, null=True)
    # The application status of the volunteer.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    # The ID of the corresponding contact in HubSpot, once created.
    hubspot_id = models.CharField(max_length=100, blank=True, null=True, unique=True)

    def __str__(self):
        """
        Returns a string representation of the volunteer, which is their name.
        This is used in the Django admin interface and other places where the
        object needs to be represented as a string.
        """
        return self.name
