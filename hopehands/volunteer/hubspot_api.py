# hopehands/volunteer/hubspot_api.py

"""
File Purpose: A dedicated module for all communication with the HubSpot API.

This file acts as a "wrapper" or "service layer" for the HubSpot API. Its
purpose is to centralize all the code that talks to HubSpot in one place. This
is a very good practice for several reasons:
1. Organization: We know exactly where to look for any HubSpot-related code.
2. Reusability: We can use the methods in this class from anywhere in our
   application (e.g., from `api_views.py`) without rewriting the same logic.
3. Maintainability: If HubSpot changes its API, we only need to update the code
   in this one file, not all over the project.
4. Abstraction: The rest of our application doesn't need to know the complex
   details of how the HubSpot API works. It can just call simple methods like
   `create_contact`.

Relationship to other files:
- `api_views.py`: This is the primary consumer of this file. The views in that
  file create an instance of the `HubspotAPI` class and call its methods to
  sync data with HubSpot.
- `settings.py`: This file gets the `HUBSPOT_PRIVATE_APP_TOKEN` from the Django
  settings, which is where we store sensitive credentials.
"""

# Import Django's settings to safely access our API key.
from django.conf import settings
# Import the official HubSpot library and specific classes we need.
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput, PublicObjectSearchRequest, Filter, FilterGroup
from hubspot.crm.contacts.exceptions import ApiException
# Import Python's logging tool to record errors.
import logging

# Get a logger instance, which allows us to write messages to the console or a file.
logger = logging.getLogger(__name__)

# This class contains all the methods for interacting with the HubSpot Contacts API.
class HubspotAPI:
    """
    A wrapper class for the HubSpot API client.
    This class provides methods for all the HubSpot contact operations required by the
    HopeHands application. It initializes the HubSpot client with the access token
    from the Django settings.
    """
    # This is the "constructor" method. It's called automatically whenever a
    # new instance of the HubspotAPI class is created.
    def __init__(self):
        """
        Initializes the HubSpot API client.
        The access token is retrieved from the Django settings, which in turn
        loads it from the .env file.
        """
        # This line creates the official HubSpot client using our secret API key.
        # The client object will handle all the authentication and network requests for us.
        self.client = HubSpot(access_token=settings.HUBSPOT_PRIVATE_APP_TOKEN)

    # This method creates a single new contact in HubSpot.
    def create_contact(self, email, first_name, last_name, phone_number, preferred_volunteer_role, availability, how_did_you_hear_about_us):
        """
        Creates a new contact in HubSpot using the volunteer's details.

        Args:
            email (str): The volunteer's email address.
            first_name (str): The volunteer's first name.
            last_name (str): The volunteer's last name.
            phone_number (str): The volunteer's phone number.
            preferred_volunteer_role (str): The volunteer's preferred role.
            availability (str): The volunteer's availability.
            how_did_you_hear_about_us (str): How the volunteer heard about HopeHands.

        Returns:
            The created contact object from HubSpot, or None if creation fails.
        """
        # The HubSpot API expects data to be formatted as a dictionary of "properties".
        # We build this dictionary using the arguments passed to the method.
        # The keys (e.g., "email", "firstname") must match the property names in HubSpot.
        properties = {
            "email": email,
            "firstname": first_name,
            "lastname": last_name,
            "phone": phone_number,
            "lifecyclestage": "lead",  # We set a default lifecycle stage for new contacts.
            "preferred_volunteer_role": preferred_volunteer_role,
            "availability": availability,
            "how_did_you_hear_about_us": how_did_you_hear_about_us,
        }
        # The HubSpot API client expects the properties to be wrapped in a SimplePublicObjectInput.
        simple_public_object_input = SimplePublicObjectInput(properties=properties)
        try:
            # This is the actual API call. We use the client we created in `__init__`
            # and call the `create` method from the contacts API.
            api_response = self.client.crm.contacts.basic_api.create(
                simple_public_object_input_for_create=simple_public_object_input
            )
            # This line logs a success message to the console for debugging purposes.
            logger.info(f"Successfully created contact in HubSpot: {api_response}")
            # If the call is successful, we return the response from HubSpot,
            # which contains the new contact's ID and data.
            return api_response
        except ApiException as e:
            # If anything goes wrong with the API call (e.g., invalid data, server error),
            # the HubSpot library will raise an `ApiException`.
            # We "catch" this exception so our app doesn't crash.
            logger.error("Exception when creating contact in HubSpot", exc_info=True)
            # We return `None` to signal that the creation failed.
            return None

    # This method is not currently used by the main application but is kept for utility.
    def get_all_contacts(self):
        """
        Retrieves all contacts from HubSpot. Currently for utility or future use.

        Returns:
            list: A list of HubSpot contact objects. Returns an empty list if
                  the API call fails.
        """
        try:
            # Define the specific pieces of information (properties) we want to retrieve for each contact.
            properties = ["firstname", "lastname", "email", "phone"]
            # Call the API to get a "page" of contacts (up to 100).
            api_response = self.client.crm.contacts.basic_api.get_page(
                limit=100, properties=properties
            )
            # The actual list of contacts is inside the 'results' attribute of the response.
            return api_response.results
        except ApiException as e:
            # If the API call fails, log the error and return an empty list.
            logger.error("Exception when getting contacts from HubSpot", exc_info=True)
            return []

    # This method is not currently used by the main application but is kept for utility.
    def get_contact(self, contact_id):
        """
        Retrieves a single contact by its ID from HubSpot. Currently for utility or future use.

        Args:
            contact_id (int): The ID of the contact to retrieve.

        Returns:
            SimplePublicObject or None: The contact object from HubSpot, or None
                                        if the contact is not found or an error
                                        occurs.
        """
        try:
            # Define the properties we want to retrieve for this specific contact.
            properties = [
                "firstname", "lastname", "email", "phone",
                "lifecyclestage", "preferred_volunteer_role",
                "availability", "how_did_you_hear_about_us"
            ]
            # Call the API to get a single contact by its unique HubSpot ID.
            contact = self.client.crm.contacts.basic_api.get_by_id(
                contact_id, properties=properties
            )
            # Return the found contact object.
            return contact
        except ApiException as e:
            # If the API call fails (e.g., contact not found), log the error and return None.
            logger.error(f"Exception when getting contact {contact_id} from HubSpot", exc_info=True)
            return None

    # This method updates an existing contact in HubSpot.
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
        # We wrap the new properties in the required object, just like in the create method.
        simple_public_object_input = SimplePublicObjectInput(properties=properties)
        try:
            # We call the `update` method, providing the ID of the contact to change
            # and the new data.
            api_response = self.client.crm.contacts.basic_api.update(
                contact_id=contact_id,
                simple_public_object_input=simple_public_object_input
            )
            # Return the updated contact object from HubSpot.
            return api_response
        except ApiException as e:
            # If it fails, we log the error and return None.
            logger.error(f"Exception when updating contact {contact_id} in HubSpot", exc_info=True)
            return None

    # This method "archives" (soft-deletes) a contact in HubSpot.
    def delete_contact(self, contact_id):
        """
        Deletes a contact from HubSpot.
        Note: In the HubSpot API, this is an "archive" operation, not a permanent delete.

        Args:
            contact_id (int): The ID of the contact to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            # We call the `archive` method, which simply needs the ID of the contact to delete.
            self.client.crm.contacts.basic_api.archive(contact_id)
            # If the call completes without an error, we return True.
            return True
        except ApiException as e:
            # If it fails, we log the error and return False.
            logger.error(f"Exception when deleting contact {contact_id} from HubSpot", exc_info=True)
            return False

    # This method creates multiple contacts at once.
    def batch_create_contacts(self, contacts_properties):
        """
        Creates multiple contacts in HubSpot in a single batch request. This is
        much more efficient than creating them one by one in a loop.

        Args:
            contacts_properties (list): A list of dictionaries, where each
                                        dictionary contains the properties for
                                        a new contact.

        Returns:
            BatchResponseSimplePublicObject or None: The response from the batch
                                                     API call, or None if the
                                                     call fails.
        """
        # The batch API requires a list of objects, where each object contains the properties for one contact.
        # This line uses a "list comprehension" to build that list.
        inputs = [{"properties": props} for props in contacts_properties]
        try:
            # This is the batch API call. We call the `create` method from the batch API.
            api_response = self.client.crm.contacts.batch_api.create(
                batch_input_simple_public_object_batch_input_for_create={"inputs": inputs}
            )
            # If successful, we return the response from HubSpot.
            return api_response
        except ApiException as e:
            # If it fails, we log the error and return None.
            logger.error("Exception when batch creating contacts in HubSpot", exc_info=True)
            return None

    # This method is not currently used by the main application but is kept for utility.
    def search_contacts(self, query):
        """
        Searches for contacts by first name, last name, email, or phone in HubSpot.
        Currently for utility or future use.

        Args:
            query (str): The search term to look for.

        Returns:
            A list of HubSpot contact objects that match the search query, or an
            empty list if an error occurs.
        """
        try:
            # The search API uses "filters" to define the search criteria.
            # We create a filter for each property we want to search.
            filter_firstname = Filter(property_name="firstname", operator="CONTAINS_TOKEN", value=query)
            filter_lastname = Filter(property_name="lastname", operator="CONTAINS_TOKEN", value=query)
            filter_email = Filter(property_name="email", operator="EQ", value=query)
            filter_phone = Filter(property_name="phone", operator="EQ", value=query)

            # To create an "OR" search (e.g., find where firstname OR lastname matches),
            # we need to put each filter in its own "FilterGroup".
            filter_group_firstname = FilterGroup(filters=[filter_firstname])
            filter_group_lastname = FilterGroup(filters=[filter_lastname])
            filter_group_email = FilterGroup(filters=[filter_email])
            filter_group_phone = FilterGroup(filters=[filter_phone])

            # The search request object contains the list of filter groups.
            # The API will find results that match ANY of these groups.
            search_request = PublicObjectSearchRequest(
                filter_groups=[
                    filter_group_firstname,
                    filter_group_lastname,
                    filter_group_email,
                    filter_group_phone
                ],
                properties=["firstname", "lastname", "email", "phone"], # The properties to return for found contacts.
                limit=100
            )

            # Perform the search API call.
            api_response = self.client.crm.contacts.search_api.do_search(
                public_object_search_request=search_request
            )
            # Return the list of results.
            return api_response.results
        except ApiException as e:
            # If the search fails, log the error and return an empty list.
            logger.error(f"Exception when searching for contacts with query '{query}'", exc_info=True)
            return []
