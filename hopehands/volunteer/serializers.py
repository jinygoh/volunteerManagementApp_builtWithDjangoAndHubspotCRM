from rest_framework import serializers
from .models import Volunteer

class VolunteerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Volunteer model.
    """
    class Meta:
        model = Volunteer
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'preferred_volunteer_role',
            'availability',
            'how_did_you_hear_about_us',
            'status',
            'hubspot_id'
        ]
        read_only_fields = ['status', 'hubspot_id']
