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
from .hubspot_api import HubspotAPI

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
        This changes the volunteer's status to 'approved' and triggers the sync to HubSpot.
        """
        volunteer = self.get_object()
        if volunteer.status == 'pending':
            volunteer.status = 'approved'

            # Sync to HubSpot upon approval
            hubspot_api = HubspotAPI()
            api_response = hubspot_api.create_contact(
                email=volunteer.email,
                first_name=volunteer.first_name,
                last_name=volunteer.last_name,
                phone_number=volunteer.phone_number,
                preferred_volunteer_role=volunteer.preferred_volunteer_role,
                availability=volunteer.availability,
                how_did_you_hear_about_us=volunteer.how_did_you_hear_about_us,
            )
            # If the sync is successful, save the returned HubSpot ID
            if api_response:
                volunteer.hubspot_id = api_response.id

            volunteer.save()
            return Response({'status': 'volunteer approved'}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'status': 'This volunteer is not in a pending state.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        """
        Updates a volunteer's details and syncs the changes to HubSpot if the
        volunteer has already been approved and has a HubSpot ID.
        """
        # First, perform the default update behavior from the parent class.
        # This will update the volunteer instance in the local database.
        response = super().update(request, *args, **kwargs)

        # If the update was successful (HTTP 200 OK), proceed to sync with HubSpot.
        if response.status_code == status.HTTP_200_OK:
            # Retrieve the updated volunteer instance.
            volunteer = self.get_object()

            # If the volunteer has a HubSpot ID, it means they have been synced before.
            if volunteer.hubspot_id:
                # Prepare the data for the HubSpot API call.
                hubspot_api = HubspotAPI()
                properties = {
                    "email": volunteer.email,
                    "firstname": volunteer.first_name,
                    "lastname": volunteer.last_name,
                    "phone": volunteer.phone_number,
                    "preferred_volunteer_role": volunteer.preferred_volunteer_role,
                    "availability": volunteer.availability,
                    "how_did_you_hear_about_us": volunteer.how_did_you_hear_about_us,
                }
                # Call the HubSpot API to update the contact.
                hubspot_api.update_contact(volunteer.hubspot_id, properties)

        return response

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
    This process directly approves the volunteers, creates them in the local
    database, and performs a batch sync to HubSpot.
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
                decoded_file = file_content.decode('utf-8')
            else:
                decoded_file = file_content
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)

            volunteers_to_create = []
            contacts_for_hubspot = []
            errors = []

            for row in reader:
                email = row.get('Email')
                if not email:
                    errors.append(f"Skipping row due to missing email: {row}")
                    continue

                volunteers_to_create.append(
                    Volunteer(
                        first_name=row.get('First Name', ''),
                        last_name=row.get('Last Name', ''),
                        email=email,
                        phone_number=row.get('Phone Number', ''),
                        preferred_volunteer_role=row.get('Preferred Volunteer Role', ''),
                        availability=row.get('Availability', ''),
                        how_did_you_hear_about_us=row.get('How did you hear about us?', ''),
                        status='approved'
                    )
                )

                contacts_for_hubspot.append({
                    "email": email,
                    "firstname": row.get('First Name', ''),
                    "lastname": row.get('Last Name', ''),
                    "phone": row.get('Phone Number', ''),
                    "preferred_volunteer_role": row.get('Preferred Volunteer Role', ''),
                    "availability": row.get('Availability', ''),
                    "how_did_you_hear_about_us": row.get('How did you hear about us?', ''),
                    "lifecyclestage": "lead",
                })

            if not volunteers_to_create:
                return Response({"error": "No valid volunteer data found in CSV.", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

            created_volunteers = Volunteer.objects.bulk_create(volunteers_to_create)

            email_to_volunteer_map = {v.email: v for v in created_volunteers}

            hubspot_api = HubspotAPI()
            hubspot_response = hubspot_api.batch_create_contacts(contacts_for_hubspot)

            synced_count = 0
            if hubspot_response and hubspot_response.status == 'COMPLETE':
                volunteers_to_update = []
                for contact in hubspot_response.results:
                    volunteer = email_to_volunteer_map.get(contact.properties['email'])
                    if volunteer:
                        volunteer.hubspot_id = contact.id
                        volunteers_to_update.append(volunteer)
                        synced_count += 1

                Volunteer.objects.bulk_update(volunteers_to_update, ['hubspot_id'])

            return Response({
                "status": f"{len(created_volunteers)} volunteers created locally. {synced_count} synced to HubSpot.",
                "errors": errors
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Failed to process CSV file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
After 