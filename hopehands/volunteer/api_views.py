from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Volunteer
from .serializers import VolunteerSerializer
from .hubspot_api import HubspotAPI

class VolunteerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows volunteers to be viewed or edited.
    """
    queryset = Volunteer.objects.all().order_by('-id')
    serializer_class = VolunteerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Approve a volunteer and sync them to HubSpot.
        """
        volunteer = self.get_object()
        if volunteer.status == 'pending':
            volunteer.status = 'approved'

            # Sync to HubSpot
            hubspot_api = HubspotAPI()
            api_response = hubspot_api.create_contact(
                email=volunteer.email,
                name=volunteer.name,
                phone_number=volunteer.phone_number,
                preferred_volunteer_role=volunteer.preferred_volunteer_role,
                availability=volunteer.availability,
                how_did_you_hear_about_us=volunteer.how_did_you_hear_about_us,
            )
            if api_response:
                volunteer.hubspot_id = api_response.id

            volunteer.save()
            return Response({'status': 'volunteer approved'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'volunteer not in pending state'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Reject a volunteer.
        """
        volunteer = self.get_object()
        if volunteer.status == 'pending':
            volunteer.status = 'rejected'
            volunteer.save()
            return Response({'status': 'volunteer rejected'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'volunteer not in pending state'}, status=status.HTTP_400_BAD_REQUEST)

class VolunteerPublicCreateView(generics.CreateAPIView):
    """
    Public API endpoint for creating a new volunteer (signup).
    No authentication required.
    """
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [] # No permissions, public endpoint

class LoginView(APIView):
    """
    API view for user login.
    """
    permission_classes = [] # No permissions, public endpoint

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'status': 'success', 'user': user.username}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
