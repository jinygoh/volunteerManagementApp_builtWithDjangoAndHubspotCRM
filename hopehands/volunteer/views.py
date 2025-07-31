from django.shortcuts import render, redirect
from .forms import VolunteerForm
from django.conf import settings
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput
from hubspot.crm.contacts.exceptions import ApiException
import logging

logger = logging.getLogger(__name__)

def volunteer_signup(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            volunteer = form.save()
            try:
                hubspot = HubSpot(access_token=settings.HUBSPOT_PRIVATE_APP_TOKEN)
                properties = {
                    "email": volunteer.email,
                    "firstname": volunteer.name,
                    "phone": volunteer.phone_number,
                    "lifecyclestage": "lead",
                    "preferred_volunteer_role": volunteer.preferred_volunteer_role,
                    "availability": volunteer.availability,
                    "how_did_you_hear_about_us": volunteer.how_did_you_hear_about_us,
                }
                print("Creating HubSpot contact with properties:", properties)
                simple_public_object_input = SimplePublicObjectInput(properties=properties)
                api_response = hubspot.crm.contacts.basic_api.create(
                    simple_public_object_input_for_create=simple_public_object_input
                )
                logger.info(f"Successfully created contact in HubSpot: {api_response}")
            except ApiException as e:
                logger.error("Exception when creating contact in HubSpot", exc_info=True)
            return redirect('success')
    else:
        form = VolunteerForm()
    return render(request, 'volunteer/signup.html', {'form': form})

def success(request):
    return render(request, 'volunteer/success.html')
