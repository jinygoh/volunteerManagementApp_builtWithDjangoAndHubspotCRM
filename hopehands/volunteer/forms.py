# Import the forms module from Django.
from django import forms
# Import the Volunteer model from the current directory's models.py.
from .models import Volunteer

# Define a form for the Volunteer model.
# ModelForm is a helper class that lets you create a Form class from a Django model.
class VolunteerForm(forms.ModelForm):
    """
    This form is used to create and update Volunteer objects.
    It automatically generates form fields based on the Volunteer model.
    """
    # The Meta class provides configuration for the form.
    class Meta:
        # Specify the model to be used for this form.
        model = Volunteer
        # Specify which fields from the model should be included in the form.
        # '__all__' is a shortcut to include all fields.
        fields = '__all__'
