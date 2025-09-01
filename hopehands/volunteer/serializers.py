"""
Serializers for the Volunteer App.

This module contains the serializers used by the Django REST Framework to convert
complex data types, such as Django model instances, into native Python datatypes
that can then be easily rendered into JSON, XML, or other content types.
Serializers also provide deserialization, allowing parsed data to be converted
back into complex types after first validating the incoming data.
"""
from rest_framework import serializers
from .models import Volunteer

class VolunteerSerializer(serializers.ModelSerializer):
    """
    Serializes Volunteer model instances into JSON format.

    This serializer is used by the API views to control which fields of the
    Volunteer model are exposed in the API and how they are represented.
    """
    class Meta:
        """
        Meta class for the VolunteerSerializer.

        Defines the model to be serialized and the fields to be included in the
        serialized representation.
        """
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
            'status'
        ]
        # The 'status' field is managed by the backend logic (e.g., the
        # approval workflow) and should not be directly editable by API clients.
        read_only_fields = ['status']
