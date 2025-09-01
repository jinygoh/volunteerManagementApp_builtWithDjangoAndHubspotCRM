from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
import csv
import io

from django.db.models import Count

from .models import Volunteer
from .serializers import VolunteerSerializer


class VolunteerVisualizationView(APIView):
    """
    API endpoint to provide data for visualization.
    Returns the count of volunteers for each 'preferred_volunteer_role'.
    Requires admin authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Returns aggregated data on volunteer roles.
        """
        role_data = (
            Volunteer.objects
            .values('preferred_volunteer_role')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        return Response(role_data)

class VolunteerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for administrators to manage volunteers.
    Provides full CRUD functionality and custom actions for approval/rejection.
    Requires authentication.
    """
    queryset = Volunteer.objects.all().order_by('-id')
    serializer_class = VolunteerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        """
        Custom action to approve a volunteer application.
        This changes the volunteer's status to 'approved'.
        """
        volunteer = self.get_object()
        if volunteer.status == 'pending':
            volunteer.status = 'approved'
            volunteer.save()
            return Response({'status': 'volunteer approved'}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'status': 'This volunteer is not in a pending state.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a volunteer from the local database.
        """
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Updates a volunteer's details.
        """
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        """
        Custom action to reject a volunteer application.
        This simply changes the volunteer's status to 'rejected'.
        """
        volunteer = self.get_object()
        if volunteer.status == 'pending':
            volunteer.status = 'rejected'
            volunteer.save()
            return Response({'status': 'volunteer rejected'}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'status': 'This volunteer is not in a pending state.'},
                status=status.HTTP_400_BAD_REQUEST
            )

class VolunteerPublicCreateView(generics.CreateAPIView):
    """
    Public API endpoint for creating a new volunteer (the signup form).
    This view does not require authentication. By setting authentication_classes
    to [], we ensure that this endpoint never tries to validate a token, even
    if an invalid or expired one is sent by the browser. This makes the
    endpoint truly public.
    """
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    authentication_classes = [] # No authentication for this public view
    permission_classes = [] # No permissions ensures this endpoint is public

class VolunteerCSVUploadAPIView(APIView):
    """
    API endpoint for batch uploading volunteers from a CSV file.
    This process directly approves the volunteers and creates them in the local
    database.
    Requires admin authentication.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        if 'file' not in request.data:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        file_obj = request.data['file']
        try:
            # Handle both in-memory text files (from tests) and binary files (from uploads)
            file_content = file_obj.read()
            if isinstance(file_content, bytes):
                # Use 'utf-8-sig' to handle the BOM (Byte Order Mark)
                decoded_file = file_content.decode('utf-8-sig')
            else:
                decoded_file = file_content
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)

            # Normalize the fieldnames to be lowercase and use underscores for consistency
            if reader.fieldnames:
                reader.fieldnames = [field.lower().replace(' ', '_').replace('?', '') for field in reader.fieldnames]

            volunteers_to_create = []
            errors = []

            for row in reader:
                email = row.get('email')
                if not email:
                    errors.append(f"Skipping row due to missing email: {row}")
                    continue

                # Handle name, which can be in 'name' or 'first_name'/'last_name' columns
                first_name = row.get('first_name', '')
                last_name = row.get('last_name', '')
                if not first_name and not last_name:
                    name = row.get('name', '')
                    if name:
                        parts = name.split(' ', 1)
                        first_name = parts[0]
                        last_name = parts[1] if len(parts) > 1 else ''

                # Get other fields using normalized keys
                phone_number = row.get('phone_number', '')
                preferred_volunteer_role = row.get('preferred_volunteer_role', '')
                availability = row.get('availability', '')
                how_did_you_hear_about_us = row.get('how_did_you_hear_about_us', '')

                volunteers_to_create.append(
                    Volunteer(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone_number=phone_number,
                        preferred_volunteer_role=preferred_volunteer_role,
                        availability=availability,
                        how_did_you_hear_about_us=how_did_you_hear_about_us,
                        status='approved'
                    )
                )

            if not volunteers_to_create:
                return Response({"error": "No valid volunteer data found in CSV.", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

            created_count = len(volunteers_to_create)
            Volunteer.objects.bulk_create(volunteers_to_create)

            return Response({
                "status": f"{created_count} volunteers created locally.",
                "errors": errors
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Failed to process CSV file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
