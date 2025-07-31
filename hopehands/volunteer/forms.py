from django import forms
from .models import Volunteer

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = [
            'name',
            'email',
            'phone_number',
            'preferred_volunteer_role',
            'availability',
            'how_did_you_hear_about_us'
        ]
