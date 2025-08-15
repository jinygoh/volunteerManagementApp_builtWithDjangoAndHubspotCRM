from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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
                name=volunteer.name,
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

