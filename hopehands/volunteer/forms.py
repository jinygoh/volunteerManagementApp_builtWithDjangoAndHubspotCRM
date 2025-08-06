# hopehands/volunteer/forms.py

"""
This file defines the forms used in the volunteer application.
Django's forms framework provides a powerful way to handle HTML forms. It can
handle rendering forms as HTML, validating submitted data, and processing the
data.

This file contains two forms:
- VolunteerForm: A ModelForm for creating and updating Volunteer objects.
- CSVUploadForm: A simple form for handling CSV file uploads.
"""

from django import forms
from .models import Volunteer

class VolunteerForm(forms.ModelForm):
    """
    A form for creating and updating Volunteer instances.
    This is a ModelForm, which means it is automatically generated from the
    Volunteer model. This avoids duplicating the field definitions.
    """
    class Meta:
        """
        The Meta class provides configuration for the ModelForm.
        - model: The model to base the form on.
        - fields: The fields from the model to include in the form.
        """
        model = Volunteer
        fields = [
            'name',
            'email',
            'phone_number',
            'preferred_volunteer_role',
            'availability',
            'how_did_you_hear_about_us'
        ]

class CSVUploadForm(forms.Form):
    """
    A simple form for uploading a CSV file.
    It contains a single FileField to handle the file upload.
    """
    csv_file = forms.FileField(label="Select a CSV file")
