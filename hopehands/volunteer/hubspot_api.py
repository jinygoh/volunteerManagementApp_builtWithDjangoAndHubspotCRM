# hopehands/volunteer/hubspot_api.py

"""
This file provides a dedicated service for interacting with the HubSpot API.
It encapsulates all the logic for making API calls to HubSpot, such as creating,
retrieving, updating, and deleting contacts. This approach isolates the HubSpot-related
code from the Django views, making the views cleaner and the HubSpot integration
easier to manage and test.

This service is used by the views in `views.py` to perform CRUD operations on
HubSpot contacts.
"""

from django.conf import settings
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput
from hubspot.crm.contacts.exceptions import ApiException
import logging

# Standard logger for this module
logger = logging.getLogger(__name__)

class HubspotAPI:
    """
    A wrapper class for the HubSpot API client.
    This class provides methods for all the HubSpot contact operations required by the
    HopeHands application. It initializes the HubSpot client with the access token
    from the Django settings.
    """
    def __init__(self):
        """
        Initializes the HubSpot API client.
        The access token is retrieved from the Django settings, which in turn
        loads it from the .env file.
        """
        self.client = HubSpot(access_token=settings.HUBSPOT_PRIVATE_APP_TOKEN)

    def create_contact(self, email, name, phone_number, preferred_volunteer_role, availability, how_did_you_hear_about_us):
        """
        Creates a new contact in HubSpot.

        Args:
            email (str): The email address of the contact.
            name (str): The first name of the contact.
            phone_number (str): The phone number of the contact.
            preferred_volunteer_role (str): The preferred volunteer role.
            availability (str): The contact's availability.
            how_did_you_hear_about_us (str): How the contact heard about HopeHands.

        Returns:
            SimplePublicObject or None: The created contact object from HubSpot,
                                        or None if the creation failed.
        """
        properties = {
            "email": email,
            "firstname": name,
            "phone": phone_number,
            "lifecyclestage": "lead",  # Default lifecycle stage for new volunteers
            "preferred_volunteer_role": preferred_volunteer_role,
            "availability": availability,
            "how_did_you_hear_about_us": how_did_you_hear_about_us,
        }
        # The HubSpot API client expects the properties to be wrapped in a SimplePublicObjectInput
        simple_public_object_input = SimplePublicObjectInput(properties=properties)
        try:
            # Make the API call to create the contact
            api_response = self.client.crm.contacts.basic_api.create(
                simple_public_object_input_for_create=simple_public_object_input
            )
            logger.info(f"Successfully created contact in HubSpot: {api_response}")
            return api_response
        except ApiException as e:
            # Log any exceptions that occur during the API call
            logger.error("Exception when creating contact in HubSpot", exc_info=True)
            return None

    def get_all_contacts(self):
        """
        Retrieves all contacts from HubSpot.

        Returns:
            list: A list of HubSpot contact objects. Returns an empty list if
                  the API call fails.
        """
        try:
            # Get a page of contacts (default limit is 10, max is 100)
            api_response = self.client.crm.contacts.basic_api.get_page(limit=100)
            # The contacts are in the 'results' attribute of the response
            return api_response.results
        except ApiException as e:
            logger.error("Exception when getting contacts from HubSpot", exc_info=True)
            return []

    def get_contact(self, contact_id):
        """
        Retrieves a single contact by its ID from HubSpot.

        Args:
            contact_id (int): The ID of the contact to retrieve.

        Returns:
            SimplePublicObject or None: The contact object from HubSpot, or None
                                        if the contact is not found or an error
                                        occurs.
        """
        try:
            # Get the contact by its ID
            contact = self.client.crm.contacts.basic_api.get_by_id(contact_id)
            return contact
        except ApiException as e:
            logger.error(f"Exception when getting contact {contact_id} from HubSpot", exc_info=True)
            return None

    def update_contact(self, contact_id, properties):
        """
        Updates an existing contact in HubSpot.

        Args:
            contact_id (int): The ID of the contact to update.
            properties (dict): A dictionary of the contact properties to update.

        Returns:
            SimplePublicObject or None: The updated contact object from HubSpot,
                                        or None if the update fails.
        """
        simple_public_object_input = SimplePublicObjectInput(properties=properties)
        try:
            # Make the API call to update the contact
            api_response = self.client.crm.contacts.basic_api.update(
                contact_id=contact_id,
                simple_public_object_input=simple_public_object_input
            )
            return api_response
        except ApiException as e:
            logger.error(f"Exception when updating contact {contact_id} in HubSpot", exc_info=True)
            return None

    def delete_contact(self, contact_id):
        """
        Deletes a contact from HubSpot.
        Note: In the HubSpot API, this is an "archive" operation.

        Args:
            contact_id (int): The ID of the contact to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            # Archive (delete) the contact
            self.client.crm.contacts.basic_api.archive(contact_id)
            return True
        except ApiException as e:
            logger.error(f"Exception when deleting contact {contact_id} from HubSpot", exc_info=True)
            return False

    def batch_create_contacts(self, contacts_properties):
        """
        Creates multiple contacts in HubSpot in a single batch request.

        Args:
            contacts_properties (list): A list of dictionaries, where each
                                        dictionary contains the properties for
                                        a new contact.

        Returns:
            BatchResponseSimplePublicObject or None: The response from the batch
                                                     API call, or None if the
                                                     call fails.
        """
        # Format the properties for the batch API
        inputs = [{"properties": props} for props in contacts_properties]
        try:
            # Make the batch API call to create the contacts
            api_response = self.client.crm.contacts.batch_api.create(
                batch_input_simple_public_object_batch_input_for_create={"inputs": inputs}
            )
            return api_response
        except ApiException as e:
            logger.error("Exception when batch creating contacts in HubSpot", exc_info=True)
            return None
