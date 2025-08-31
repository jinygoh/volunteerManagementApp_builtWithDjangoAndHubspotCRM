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
    This ViewSet also handles synchronization with HubSpot:
    - Approving a volunteer creates a contact in HubSpot.
    - Updating a volunteer updates the HubSpot contact.
    - Deleting a volunteer archives the contact in HubSpot.
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

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a volunteer from the local database and also archives the
        corresponding contact in HubSpot if it exists.
        """
        volunteer = self.get_object()

        # If the volunteer has a HubSpot ID, attempt to delete them from HubSpot first.
        if volunteer.hubspot_id:
            hubspot_api = HubspotAPI()
            # The delete_contact method returns True on success, False on failure.
            # We can optionally add more robust error handling here if needed.
            hubspot_api.delete_contact(volunteer.hubspot_id)

        # After handling HubSpot, proceed with the default deletion behavior.
        return super().destroy(request, *args, **kwargs)

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
            contacts_for_hubspot = []
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

                contacts_for_hubspot.append({
                    "email": email,
                    "firstname": first_name,
                    "lastname": last_name,
                    "phone": phone_number,
                    "preferred_volunteer_role": preferred_volunteer_role,
                    "availability": availability,
                    "how_did_you_hear_about_us": how_did_you_hear_about_us,
                    "lifecyclestage": "lead",
                })

            if not volunteers_to_create:
                return Response({"error": "No valid volunteer data found in CSV.", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

            # Get the list of emails before creating the volunteers
            volunteer_emails = [v.email for v in volunteers_to_create]
            Volunteer.objects.bulk_create(volunteers_to_create)

            # After bulk creating, the volunteer instances in memory don't have their IDs.
            # We need to re-fetch them from the database to get the IDs.
            created_volunteers_with_pks = Volunteer.objects.filter(email__in=volunteer_emails)
            email_to_volunteer_map = {v.email: v for v in created_volunteers_with_pks}

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
                "status": f"{len(volunteers_to_create)} volunteers created locally. {synced_count} synced to HubSpot.",
                "errors": errors
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Failed to process CSV file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
