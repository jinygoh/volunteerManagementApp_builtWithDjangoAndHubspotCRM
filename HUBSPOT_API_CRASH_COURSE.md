# HubSpot API & Integration Crash Course

This document explains how the HopeHands application integrates with the HubSpot CRM. The integration is designed to be robust and maintainable by centralizing all HubSpot-related code into a single service class.

The core principle is that volunteer data is only sent to HubSpot **after** an administrator has explicitly approved the application.

---

## 1. The HubSpot Service Class

All direct communication with the HubSpot API is handled by the `HubspotAPI` class. This class acts as a wrapper around the official `hubspot-api-client` library. This design is a best practice because it separates the integration logic from the application's business logic (the views).

**File:** `hopehands/volunteer/hubspot_api.py`

```python
# Simplified for explanation
from django.conf import settings
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput
from hubspot.crm.contacts.exceptions import ApiException
import logging

logger = logging.getLogger(__name__)

class HubspotAPI:
    def __init__(self):
        # The client is initialized with the token from settings
        self.client = HubSpot(access_token=settings.HUBSPOT_PRIVATE_APP_TOKEN)

    def create_contact(self, email, first_name, ...):
        # 1. Prepare the data in the format HubSpot expects
        properties = {
            "email": email,
            "firstname": first_name,
            "lastname": last_name,
            # ... other properties
        }
        simple_public_object_input = SimplePublicObjectInput(properties=properties)

        try:
            # 2. Make the API call using the HubSpot client
            api_response = self.client.crm.contacts.basic_api.create(
                simple_public_object_input_for_create=simple_public_object_input
            )
            return api_response
        except ApiException as e:
            logger.error("Exception when creating contact", exc_info=True)
            return None

    def batch_create_contacts(self, contacts_properties):
        # This method handles creating multiple contacts at once
        inputs = [{"properties": props} for props in contacts_properties]
        try:
            api_response = self.client.crm.contacts.batch_api.create(
                batch_input_simple_public_object_batch_input_for_create={"inputs": inputs}
            )
            return api_response
        except ApiException as e:
            logger.error("Exception when batch creating contacts", exc_info=True)
            return None

    # ... other methods like update_contact, get_contact, etc.
```

### Key Concepts:

-   **Centralization**: All the code that knows how to "talk" to HubSpot lives in this one file. If HubSpot changes its API, we only need to update this file.
-   **Configuration**: The `__init__` method pulls the `HUBSPOT_PRIVATE_APP_TOKEN` from the Django settings, which is loaded from the `.env` file. This keeps our secret token out of the source code.
-   **Error Handling**: Each method is wrapped in a `try...except` block to catch potential `ApiException` errors from the HubSpot client, making the integration resilient.

---

## 2. How the Integration is Used

The `HubspotAPI` class is used whenever the application needs to sync data to HubSpot. This happens in two main scenarios:

### Scenario A: Admin Approves a Single Volunteer

When an administrator clicks "Approve" on the dashboard in the React application, it triggers the `approve` action in the `VolunteerViewSet`.

**File:** `hopehands/volunteer/api_views.py`

```python
# Simplified for explanation
class VolunteerViewSet(viewsets.ModelViewSet):
    # ...
    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        volunteer = self.get_object()
        if volunteer.status == 'pending':
            volunteer.status = 'approved'

            # 1. Instantiate the HubSpot service
            hubspot_api = HubspotAPI()
            # 2. Call the create_contact method with the volunteer's data
            api_response = hubspot_api.create_contact(
                email=volunteer.email,
                first_name=volunteer.first_name,
                # ... other fields
            )

            # 3. Save the returned HubSpot ID back to our database
            if api_response:
                volunteer.hubspot_id = api_response.id

            volunteer.save()
            return Response({'status': 'volunteer approved'})
```
This flow ensures that a contact is only created in HubSpot at the moment of approval. The `hubspot_id` is then saved locally to link our database record with the HubSpot contact record.

### Scenario B: Admin Uploads a CSV of Volunteers

When an administrator uploads a CSV file, the `VolunteerCSVUploadAPIView` handles the request. This view uses the `batch_create_contacts` method for efficiency.

**File:** `hopehands/volunteer/api_views.py`

```python
# Simplified for explanation
class VolunteerCSVUploadAPIView(APIView):
    def post(self, request, format=None):
        # ... code to read and parse the CSV file ...

        # contacts_for_hubspot is a list of property dictionaries
        contacts_for_hubspot = [
            {"email": "volunteer1@example.com", "firstname": "John"},
            {"email": "volunteer2@example.com", "firstname": "Jane"},
        ]

        # 1. Instantiate the service
        hubspot_api = HubspotAPI()
        # 2. Make a single batch API call
        hubspot_response = hubspot_api.batch_create_contacts(contacts_for_hubspot)

        # 3. Process the response to update local records with new HubSpot IDs
        if hubspot_response and hubspot_response.status == 'COMPLETE':
            # ... logic to match response IDs to local volunteers ...

        return Response({"status": "CSV processed"})
```
Using the batch endpoint is much more efficient than creating contacts one by one in a loop, as it reduces the number of API calls made to HubSpot.
