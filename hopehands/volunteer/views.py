# Import necessary modules from Django and other libraries.
from django.shortcuts import render, redirect  # For rendering templates and handling redirects.
from .forms import VolunteerForm  # Import the volunteer form from forms.py.
from django.conf import settings  # To access project settings, like the HubSpot API key.
from hubspot import HubSpot  # The main class for interacting with the HubSpot API.
from hubspot.crm.contacts import SimplePublicObjectInput  # For creating new contact objects.
from hubspot.crm.contacts.exceptions import ApiException  # For handling API errors.
import logging  # For logging information and errors.

# Get a logger instance for this module.
logger = logging.getLogger(__name__)

# This view handles the volunteer signup process.
def volunteer_signup(request):
    """
    Handles both the display of the signup form (GET request) and the
    processing of the submitted form data (POST request).
    """
    # If the request method is POST, it means the form has been submitted.
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request.
        form = VolunteerForm(request.POST)
        # Check if the form is valid (i.e., all required fields are filled out correctly).
        if form.is_valid():
            # Save the form data to the database, creating a new Volunteer object.
            volunteer = form.save()

            # HubSpot Integration: Create a new contact in HubSpot.
            try:
                # Initialize the HubSpot API client with the access token from settings.
                hubspot = HubSpot(access_token=settings.HUBSPOT_PRIVATE_APP_TOKEN)

                # Prepare the properties for the new HubSpot contact using data from the volunteer object.
                properties = {
                    "email": volunteer.email,
                    "firstname": volunteer.name,
                    "phone": volunteer.phone_number,
                    "lifecyclestage": "lead",  # A default lifecycle stage for new volunteers.
                    "preferred_volunteer_role": volunteer.preferred_volunteer_role,
                    "availability": volunteer.availability,
                    "how_did_you_hear_about_us": volunteer.how_did_you_hear_about_us,
                }
                # For debugging: print the properties being sent to HubSpot.
                print("Creating HubSpot contact with properties:", properties)

                # Create a HubSpot contact object with the specified properties.
                simple_public_object_input = SimplePublicObjectInput(properties=properties)

                # Make the API call to create the contact in HubSpot.
                api_response = hubspot.crm.contacts.basic_api.create(
                    simple_public_object_input_for_create=simple_public_object_input
                )
                # Log the successful creation of the contact.
                logger.info(f"Successfully created contact in HubSpot: {api_response}")

            except ApiException as e:
                # If there's an exception during the API call, log the error.
                logger.error("Exception when creating contact in HubSpot", exc_info=True)

            # Redirect the user to the success page after the form is processed.
            return redirect('success')
    else:
        # If the request method is GET, it means the user is visiting the page for the first time.
        # Create an empty form instance.
        form = VolunteerForm()

    # Render the signup page template with the form.
    # If it's a GET request, the form will be empty.
    # If it's a POST request with invalid data, the form will contain the errors.
    return render(request, 'volunteer/signup.html', {'form': form})

# This view displays the success page.
def success(request):
    """
    Renders the success page after a volunteer has successfully signed up.
    """
    # Simply render the success.html template.
    return render(request, 'volunteer/success.html')
