"""
File Purpose: Defines the API "views" for the volunteer application.

In Django, a "view" is a function or class that handles a web request and
returns a web response. These API views are specifically designed to handle
data requests (like from our React frontend) and respond with data, usually in
the JSON format. They are the core of the backend's business logic.

This file defines all the possible actions that can be performed on volunteers,
such as creating them, listing them, approving them, and syncing them with HubSpot.

Relationship to other files:
- `api_urls.py`: This file maps specific URLs (e.g., `/api/volunteers/`) to the
  view classes defined here.
- `models.py`: The views use the `Volunteer` model to interact with the database.
- `serializers.py`: The views use the `VolunteerSerializer` to convert database
  objects into JSON data to send to the frontend.
- `hubspot_api.py`: The views use the `HubspotAPI` class to communicate with the
  external HubSpot service.
"""

# Import necessary tools from the Django REST Framework and other libraries.
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
import csv
import io

# Import a database function to help with counting.
from django.db.models import Count

# Import our own application's components.
from .models import Volunteer
from .serializers import VolunteerSerializer
from .hubspot_api import HubspotAPI

# This class defines an API endpoint for the data visualization chart.
class VolunteerVisualizationView(APIView):
    """
    API endpoint to provide data for the visualization chart on the frontend.
    It calculates how many volunteers have signed up for each role.
    This endpoint is protected and can only be accessed by a logged-in admin.
    """
    # This line ensures that only authenticated users (admins) can access this view.
    permission_classes = [IsAuthenticated]

    # This function handles GET requests, which are used to retrieve data.
    def get(self, request, format=None):
        """
        Processes a request to get data for the volunteer roles chart.
        """
        # This is a database query. It groups all volunteers by their 'preferred_volunteer_role',
        # counts how many volunteers are in each group, and orders the results from most to least popular.
        role_data = (
            Volunteer.objects
            .values('preferred_volunteer_role') # 1. Group by role.
            .annotate(count=Count('id'))      # 2. Count volunteers in each group.
            .order_by('-count')               # 3. Order by the count.
        )
        # The data is returned to the frontend as a JSON response.
        return Response(role_data)

# This class is a "ViewSet," which is a powerful way to create a full set of
# standard API actions (Create, Read, Update, Delete) for a model.
class VolunteerViewSet(viewsets.ModelViewSet):
    """
    The main API endpoint for administrators to manage volunteers.
    This provides full CRUD (Create, Read, Update, Delete) functionality and
    includes our own custom actions for the approval/rejection workflow.
    This ViewSet is the central point for all HubSpot synchronization logic.
    """
    # This tells the ViewSet to get all Volunteer objects from the database, ordered by newest first.
    queryset = Volunteer.objects.all().order_by('-id')
    # This tells the ViewSet to use our VolunteerSerializer to convert the data.
    serializer_class = VolunteerSerializer
    # This ensures only logged-in admins can use these endpoints.
    permission_classes = [IsAuthenticated]

    # This decorator creates a new, custom action named "approve" for our ViewSet.
    # It will be accessible at a URL like `/api/volunteers/{id}/approve/`.
    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        """
        Custom action to approve a PENDING volunteer application.
        This changes the volunteer's status to 'approved' and triggers the
        process to create a new contact in HubSpot.
        """
        # Get the specific volunteer object based on the ID from the URL.
        volunteer = self.get_object()
        # We only want to approve volunteers who are currently 'pending'.
        if volunteer.status == 'pending':
            # Change the status in our local database.
            volunteer.status = 'approved'

            # --- Sync to HubSpot ---
            # Create an instance of our HubSpot API helper class.
            hubspot_api = HubspotAPI()
            # Call the method to create a contact in HubSpot, passing all the volunteer's details.
            api_response = hubspot_api.create_contact(
                email=volunteer.email,
                first_name=volunteer.first_name,
                last_name=volunteer.last_name,
                phone_number=volunteer.phone_number,
                preferred_volunteer_role=volunteer.preferred_volunteer_role,
                availability=volunteer.availability,
                how_did_you_hear_about_us=volunteer.how_did_you_hear_about_us,
            )
            # If the sync was successful, HubSpot returns the new contact's data.
            if api_response:
                # We save the HubSpot ID on our local volunteer record. This is crucial for future updates.
                volunteer.hubspot_id = api_response.id

            # Save the changes (the new status and HubSpot ID) to our database.
            volunteer.save()
            # Return a success message to the frontend.
            return Response({'status': 'volunteer approved'}, status=status.HTTP_200_OK)
        else:
            # If the volunteer was not pending, return an error message.
            return Response(
                {'status': 'This volunteer is not in a pending state.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    # We are overriding the default "destroy" (delete) behavior.
    def destroy(self, request, *args, **kwargs):
        """
        Deletes a volunteer from our local database AND archives their
        corresponding contact in HubSpot to keep the systems in sync.
        """
        # Get the volunteer object that is about to be deleted.
        volunteer = self.get_object()

        # Check if this volunteer has a HubSpot ID. If they do, it means they exist in HubSpot.
        if volunteer.hubspot_id:
            # Create an instance of our HubSpot API helper.
            hubspot_api = HubspotAPI()
            # Call the method to delete (archive) the contact in HubSpot.
            hubspot_api.delete_contact(volunteer.hubspot_id)

        # After dealing with HubSpot, we call the original `destroy` method
        # to finish deleting the volunteer from our local database.
        return super().destroy(request, *args, **kwargs)

    # We are also overriding the default "update" behavior.
    def update(self, request, *args, **kwargs):
        """
        Updates a volunteer's details in our local database and syncs the
        changes to HubSpot if the volunteer has a HubSpot ID.
        """
        # First, let the original `update` method do its job. This will validate
        # the incoming data and save the changes to our local database.
        response = super().update(request, *args, **kwargs)

        # The update is only synced if the local save was successful.
        if response.status_code == status.HTTP_200_OK:
            # Get the freshly updated volunteer instance.
            volunteer = self.get_object()

            # Check if they have a HubSpot ID. We only sync if they do.
            if volunteer.hubspot_id:
                # Create an instance of our HubSpot helper.
                hubspot_api = HubspotAPI()
                # Prepare the data in the format HubSpot expects.
                properties = {
                    "email": volunteer.email,
                    "firstname": volunteer.first_name,
                    "lastname": volunteer.last_name,
                    "phone": volunteer.phone_number,
                    "preferred_volunteer_role": volunteer.preferred_volunteer_role,
                    "availability": volunteer.availability,
                    "how_did_you_hear_about_us": volunteer.how_did_you_hear_about_us,
                }
                # Call the HubSpot API to update the contact, passing the ID and the new properties.
                hubspot_api.update_contact(volunteer.hubspot_id, properties)

        # Return the original response to the frontend.
        return response

    # This is another custom action, for rejecting a volunteer.
    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        """
        Custom action to reject a PENDING volunteer application.
        This simply changes the volunteer's status to 'rejected' in our
        database. No action is taken in HubSpot.
        """
        # Get the specific volunteer object.
        volunteer = self.get_object()
        # We only want to reject volunteers who are currently 'pending'.
        if volunteer.status == 'pending':
            # Change the status.
            volunteer.status = 'rejected'
            # Save the change to the database.
            volunteer.save()
            # Return a success message.
            return Response({'status': 'volunteer rejected'}, status=status.HTTP_200_OK)
        else:
            # If they were not pending, return an error.
            return Response(
                {'status': 'This volunteer is not in a pending state.'},
                status=status.HTTP_400_BAD_REQUEST
            )

# This class defines the public-facing API endpoint for the signup form.
class VolunteerPublicCreateView(generics.CreateAPIView):
    """
    Public API endpoint for creating a new volunteer (the signup form).
    This view does not require any authentication, so anyone can submit the form.
    We make it truly public by explicitly removing authentication checks.
    """
    # This view can create any volunteer object.
    queryset = Volunteer.objects.all()
    # It uses the VolunteerSerializer to validate and create the object.
    serializer_class = VolunteerSerializer
    # This line is key: it tells Django to NOT check for any authentication.
    authentication_classes = []
    # This line tells Django to NOT check for any permissions.
    permission_classes = []

# This class defines the API endpoint for the CSV bulk upload feature.
class VolunteerCSVUploadAPIView(APIView):
    """
    API endpoint for admins to batch upload volunteers from a CSV file.
    This process directly approves the volunteers, creates them in the local
    database, and performs a batch sync to create them in HubSpot.
    This is an admin-only feature.
    """
    # Only authenticated admins can use this endpoint.
    permission_classes = [IsAuthenticated]
    # These "parsers" tell Django how to handle file uploads.
    parser_classes = (MultiPartParser, FormParser)

    # This function handles POST requests, which are used to send data to the server.
    def post(self, request, format=None):
        # First, check if a file was actually included in the request.
        if 'file' not in request.data:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the file object from the request.
        file_obj = request.data['file']
        try:
            # --- File Reading and Parsing ---
            # Read the raw content of the uploaded file.
            file_content = file_obj.read()
            # Files can be encoded in different ways. We need to decode it into a standard text format (UTF-8).
            if isinstance(file_content, bytes):
                # 'utf-8-sig' is used to handle a special invisible character (BOM) that spreadsheets sometimes add.
                decoded_file = file_content.decode('utf-8-sig')
            else:
                decoded_file = file_content
            # The `csv` library needs a file-like object, so we wrap our decoded text in one.
            io_string = io.StringIO(decoded_file)
            # The `DictReader` is very useful; it reads each row of the CSV as a dictionary,
            # where the keys are the column headers.
            reader = csv.DictReader(io_string)

            # --- Data Normalization ---
            # To make our code more robust, we clean up the column headers.
            # We make them all lowercase and replace spaces with underscores.
            # e.g., "First Name" becomes "first_name".
            if reader.fieldnames:
                reader.fieldnames = [field.lower().replace(' ', '_').replace('?', '') for field in reader.fieldnames]

            # These lists will hold the data as we process the file.
            volunteers_to_create = [] # For our local database
            contacts_for_hubspot = [] # For the HubSpot batch API
            errors = []               # To keep track of any rows we have to skip.

            # --- Data Processing Loop ---
            # Loop through each row in the CSV file.
            for row in reader:
                # The email is essential. If a row doesn't have an email, we skip it.
                email = row.get('email')
                if not email:
                    errors.append(f"Skipping row due to missing email: {row}")
                    continue

                # The name might be in one column ("Name") or two ("First Name", "Last Name").
                # This logic handles both cases.
                first_name = row.get('first_name', '')
                last_name = row.get('last_name', '')
                if not first_name and not last_name:
                    name = row.get('name', '')
                    if name:
                        parts = name.split(' ', 1)
                        first_name = parts[0]
                        last_name = parts[1] if len(parts) > 1 else ''

                # Get the rest of the fields from the row using our normalized keys.
                phone_number = row.get('phone_number', '')
                preferred_volunteer_role = row.get('preferred_volunteer_role', '')
                availability = row.get('availability', '')
                how_did_you_hear_about_us = row.get('how_did_you_hear_about_us', '')

                # Create a Volunteer model instance (but don't save it to the DB yet).
                # We set the status to 'approved' directly, as this is a bulk import of approved volunteers.
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

                # Prepare the data for this volunteer in the format HubSpot's API requires.
                contacts_for_hubspot.append({
                    "email": email,
                    "firstname": first_name,
                    "lastname": last_name,
                    "phone": phone_number,
                    "preferred_volunteer_role": preferred_volunteer_role,
                    "availability": availability,
                    "how_did_you_hear_about_us": how_did_you_hear_about_us,
                    "lifecyclestage": "lead", # This is a standard HubSpot field.
                })

            # If after processing the file, we have no valid volunteers, return an error.
            if not volunteers_to_create:
                return Response({"error": "No valid volunteer data found in CSV.", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

            # --- Database and API Operations (Bulk) ---
            # Get a list of all emails before we create the volunteers.
            volunteer_emails = [v.email for v in volunteers_to_create]
            # `bulk_create` is a very efficient Django method to insert many objects into the database at once.
            Volunteer.objects.bulk_create(volunteers_to_create)

            # A quirk of `bulk_create` is that the original objects in our list don't get database IDs.
            # We need their IDs to update them with HubSpot IDs later.
            # So, we re-fetch the volunteers we just created from the database.
            created_volunteers_with_pks = Volunteer.objects.filter(email__in=volunteer_emails)
            # We put them in a dictionary mapping email to the volunteer object for easy lookup.
            email_to_volunteer_map = {v.email: v for v in created_volunteers_with_pks}

            # Now, call the HubSpot API to create all the contacts in a single batch request.
            hubspot_api = HubspotAPI()
            hubspot_response = hubspot_api.batch_create_contacts(contacts_for_hubspot)

            # --- Syncing HubSpot IDs ---
            synced_count = 0
            # If the HubSpot API call was successful...
            if hubspot_response and hubspot_response.status == 'COMPLETE':
                volunteers_to_update = []
                # Loop through the results returned by HubSpot.
                for contact in hubspot_response.results:
                    # Find the local volunteer that matches the email of the created HubSpot contact.
                    volunteer = email_to_volunteer_map.get(contact.properties['email'])
                    if volunteer:
                        # Assign the new HubSpot ID to our local volunteer object.
                        volunteer.hubspot_id = contact.id
                        volunteers_to_update.append(volunteer)
                        synced_count += 1

                # `bulk_update` is an efficient way to update a specific field on many objects at once.
                Volunteer.objects.bulk_update(volunteers_to_update, ['hubspot_id'])

            # Return a final success message to the frontend.
            return Response({
                "status": f"{len(volunteers_to_create)} volunteers created locally. {synced_count} synced to HubSpot.",
                "errors": errors
            }, status=status.HTTP_201_CREATED)

        # If any other error occurs during the process, return a generic error message.
        except Exception as e:
            return Response({"error": f"Failed to process CSV file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
