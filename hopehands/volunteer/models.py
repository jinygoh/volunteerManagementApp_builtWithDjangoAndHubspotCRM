# Import the models module from Django's database library.
from django.db import models

# Define the Volunteer model, which represents a volunteer in the database.
# Each class attribute represents a database field.
class Volunteer(models.Model):
    """
    Represents a volunteer who has signed up through the website.
    This model maps to the `volunteer_volunteer` table in the database.
    """
    # The volunteer's full name.
    name = models.CharField(max_length=100)

    # The volunteer's email address. It must be unique in the database.
    email = models.EmailField(unique=True)

    # The volunteer's phone number.
    phone_number = models.CharField(max_length=15)

    # The role the volunteer is interested in.
    preferred_volunteer_role = models.CharField(max_length=100)

    # The volunteer's availability (e.g., "Weekends", "Evenings").
    availability = models.CharField(max_length=100)

    # How the volunteer heard about the organization. This field is optional.
    how_did_you_hear_about_us = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        """
        Returns a string representation of the Volunteer object, which is used
        in the Django admin interface and other string contexts.
        """
        # Display the volunteer's name.
        return self.name
