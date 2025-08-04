from django.conf import settings
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput
from hubspot.crm.contacts.exceptions import ApiException
import logging

logger = logging.getLogger(__name__)

class HubspotAPI:
    def __init__(self):
        self.client = HubSpot(access_token=settings.HUBSPOT_PRIVATE_APP_TOKEN)

    def create_contact(self, email, name, phone_number, preferred_volunteer_role, availability, how_did_you_hear_about_us):
        properties = {
            "email": email,
            "firstname": name,
            "phone": phone_number,
            "lifecyclestage": "lead",
            "preferred_volunteer_role": preferred_volunteer_role,
            "availability": availability,
            "how_did_you_hear_about_us": how_did_you_hear_about_us,
        }
        simple_public_object_input = SimplePublicObjectInput(properties=properties)
        try:
            api_response = self.client.crm.contacts.basic_api.create(
                simple_public_object_input_for_create=simple_public_object_input
            )
            logger.info(f"Successfully created contact in HubSpot: {api_response}")
            return api_response
        except ApiException as e:
            logger.error("Exception when creating contact in HubSpot", exc_info=True)
            return None

    def get_all_contacts(self):
        try:
            api_response = self.client.crm.contacts.basic_api.get_page(limit=100)
            return api_response.results
        except ApiException as e:
            logger.error("Exception when getting contacts from HubSpot", exc_info=True)
            return []

    def get_contact(self, contact_id):
        try:
            contact = self.client.crm.contacts.basic_api.get_by_id(contact_id)
            return contact
        except ApiException as e:
            logger.error(f"Exception when getting contact {contact_id} from HubSpot", exc_info=True)
            return None

    def update_contact(self, contact_id, properties):
        simple_public_object_input = SimplePublicObjectInput(properties=properties)
        try:
            api_response = self.client.crm.contacts.basic_api.update(
                contact_id=contact_id,
                simple_public_object_input=simple_public_object_input
            )
            return api_response
        except ApiException as e:
            logger.error(f"Exception when updating contact {contact_id} in HubSpot", exc_info=True)
            return None

    def delete_contact(self, contact_id):
        try:
            self.client.crm.contacts.basic_api.archive(contact_id)
            return True
        except ApiException as e:
            logger.error(f"Exception when deleting contact {contact_id} from HubSpot", exc_info=True)
            return False

    def batch_create_contacts(self, contacts_properties):
        inputs = [{"properties": props} for props in contacts_properties]
        try:
            api_response = self.client.crm.contacts.batch_api.create(
                batch_input_simple_public_object_input={"inputs": inputs}
            )
            return api_response
        except ApiException as e:
            logger.error("Exception when batch creating contacts in HubSpot", exc_info=True)
            return None
