from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
import csv
import io

from .models import Volunteer
from .serializers import VolunteerSerializer
from .hubspot_api import HubspotAPI

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
    This view does not require authentication.
    """
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [] # No permissions ensures this endpoint is public

class VolunteerCSVUploadAPIView(APIView):
    """
    API endpoint for batch uploading volunteers from a CSV file.
    Requires admin authentication.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        if 'file' not in request.data:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        file_obj = request.data['file']
        try:
            decoded_file = file_obj.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)

            volunteers_created = 0
            errors = []
            for row in reader:
                try:
                    Volunteer.objects.create(
                        first_name=row.get('First Name', ''),
                        last_name=row.get('Last Name', ''),
                        email=row.get('Email'),
                        phone_number=row.get('Phone Number'),
                        preferred_volunteer_role=row.get('Preferred Volunteer Role'),
                        availability=row.get('Availability'),
                        how_did_you_hear_about_us=row.get('How did you hear about us?'),
                    )
                    volunteers_created += 1
                except Exception as e:
                    errors.append(f"Could not create volunteer from row: {row}. Error: {e}")

            return Response({
                "status": f"{volunteers_created} volunteers created successfully.",
                "errors": errors
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Failed to parse CSV file: {e}"}, status=status.HTTP_400_BAD_REQUEST)
