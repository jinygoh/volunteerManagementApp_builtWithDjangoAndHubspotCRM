# hopehands/volunteer/models.py

"""
File Purpose: Defines the structure of our application's data.

This file is like the blueprint for the information we want to store. In web
development, these blueprints are called "models". We define a model for each
type of data we need to keep track of. For this application, our primary piece
of data is the "Volunteer".

Relationship to other files:
- `api_views.py`: The API views use this model to know how to get data from and
  save data to the database.
- `admin.py`: This model is registered here so it can be managed in Django's
  admin interface.
- `serializers.py`: The serializer converts data from this model into a format
  (JSON) that can be easily sent over the internet to our frontend.
- `forms.py`: The forms use this model to automatically generate fields for
  users to fill out.
"""

# This line imports the necessary tools from the Django framework to create a model.
from django.db import models
from django.db.models import Q

# This defines the "Volunteer" model. Think of it as a template for every
# new volunteer that signs up. Each volunteer in our database will have the
# fields listed below.
class Volunteer(models.Model):
    """
    Represents a single volunteer applicant in our local database.

    This model acts as a temporary holding area for volunteer information. When
    someone signs up via the public form, their data is stored here with a
    "pending" status. An administrator then reviews this data before it is
    officially approved and sent to the main HubSpot CRM.
    """
    # This section defines the possible choices for the 'status' field.
    # By defining them here, we ensure that a volunteer's status can only be
    # one of these three options, preventing typos or invalid states.
    STATUS_CHOICES = (
        ('pending', 'Pending'),   # The application is new and waiting for review.
        ('approved', 'Approved'), # The application has been accepted.
        ('rejected', 'Rejected'), # The application has been declined.
    )

    # Each of the following lines defines a "field," which is like a column
    # in a spreadsheet. It tells the database what kind of information to store.

    # Stores the volunteer's first name as a line of text (a "character field").
    first_name = models.CharField(max_length=50, help_text="The volunteer's first name.")
    # Stores the volunteer's last name.
    last_name = models.CharField(max_length=50, help_text="The volunteer's last name.")
    # Stores the volunteer's email. `unique=True` ensures that no two volunteers can have the same email address.
    email = models.EmailField(unique=True, help_text="The volunteer's email address. Must be unique.")
    # Stores the volunteer's phone number.
    phone_number = models.CharField(max_length=15, help_text="The volunteer's phone number.")
    # Stores the role the volunteer is interested in (e.g., "Event Staff", "Fundraising").
    preferred_volunteer_role = models.CharField(max_length=100, help_text="The volunteer's preferred role.")
    # Stores the volunteer's stated availability (e.g., "Weekends", "Mornings").
    availability = models.CharField(max_length=100, help_text="The volunteer's availability.")
    # Stores how the volunteer found out about the organization. This field is optional.
    how_did_you_hear_about_us = models.CharField(
        max_length=200,
        blank=True, # This means the field is not required in forms.
        null=True,  # This means the database can store this value as empty.
        help_text="How the volunteer heard about the organization. Optional."
    )
    # Stores the current state of the application. It uses the STATUS_CHOICES we defined above.
    # `default='pending'` means that every new volunteer will automatically have this status.
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="The application status, used in the admin approval workflow."
    )
    # This field is very important for connecting our system to HubSpot.
    # After a volunteer is approved and a contact is created in HubSpot,
    # HubSpot gives us a unique ID for that contact. We save that ID here.
    # This allows us to update or delete the correct contact in HubSpot later.
    # It is optional because it will be empty until the volunteer is approved.
    hubspot_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Stores the HubSpot Contact ID after a volunteer is approved and synced."
    )

    # The Meta class holds extra options for the model.
    class Meta:
        # This is a database rule. It ensures that every volunteer who has a
        # `hubspot_id` must have a UNIQUE `hubspot_id`. We don't want two
        # local volunteers pointing to the same HubSpot contact.
        constraints = [
            models.UniqueConstraint(
                fields=['hubspot_id'],
                condition=~models.Q(hubspot_id=None),
                name='unique_hubspot_id_when_not_null'
            )
        ]

    # This is a standard Python method. We define it to give a human-readable
    # name for each volunteer object. For example, when viewing volunteers in
    # the Django admin area, they will be listed by their full name.
    def __str__(self):
        """Returns the full name of the volunteer for display purposes."""
        return f"{self.first_name} {self.last_name}"
