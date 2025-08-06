# hopehands/volunteer/views.py

"""
This file contains the view functions for the volunteer application.
Views are responsible for handling web requests and returning web responses.
They contain the main application logic, processing user input, interacting with
the database (via models) and external APIs (via services like hubspot_api.py),
and rendering templates to generate the HTML that users see in their browsers.

This file defines views for all the CRUD (Create, Read, Update, Delete) operations
on volunteers, as well as the batch CSV upload functionality.
"""

from django.shortcuts import render, redirect
from .forms import VolunteerForm, CSVUploadForm
from .hubspot_api import HubspotAPI
from .models import Volunteer
import logging
import csv
import io

# Standard logger for this module
logger = logging.getLogger(__name__)

def volunteer_signup(request):
    """
    Handles the volunteer signup form.
    - On GET request, it displays an empty signup form.
    - On POST request, it processes the submitted form data. If the form is valid,
      it saves the new volunteer to the local database, creates a corresponding
      contact in HubSpot via the HubspotAPI service, and then redirects to a
      success page.

    Template: 'volunteer/signup.html'
    """
    # If the form is being submitted
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        # Check if the form data is valid
        if form.is_valid():
            # Save the new volunteer to the local database
            volunteer = form.save()
            # Instantiate our HubSpot API service
            hubspot_api = HubspotAPI()
            # Create the contact in HubSpot
            hubspot_api.create_contact(
                email=volunteer.email,
                name=volunteer.name,
                phone_number=volunteer.phone_number,
                preferred_volunteer_role=volunteer.preferred_volunteer_role,
                availability=volunteer.availability,
                how_did_you_hear_about_us=volunteer.how_did_you_hear_about_us,
            )
            # Redirect to the success page
            return redirect('success')
    # If it's a GET request, create an empty form
    else:
        form = VolunteerForm()
    # Render the signup page with the form
    return render(request, 'volunteer/signup.html', {'form': form})

def success(request):
    """
    Displays a simple success page.
    This page is shown after a volunteer successfully signs up.

    Template: 'volunteer/success.html'
    """
    return render(request, 'volunteer/success.html')

def volunteer_list(request):
    """
    Displays a list of all volunteers.
    It fetches all contacts from HubSpot using the HubspotAPI service and
    passes them to the template to be displayed in a table.

    Template: 'volunteer/volunteer_list.html'
    """
    hubspot_api = HubspotAPI()
    contacts = hubspot_api.get_all_contacts()
    return render(request, 'volunteer/volunteer_list.html', {'contacts': contacts})

def volunteer_detail(request, contact_id):
    """
    Displays the details of a single volunteer.
    It takes a contact_id, fetches the corresponding contact from HubSpot,
    and displays their properties.

    Template: 'volunteer/volunteer_detail.html'
    """
    hubspot_api = HubspotAPI()
    contact = hubspot_api.get_contact(contact_id)
    return render(request, 'volunteer/volunteer_detail.html', {'contact': contact})

def volunteer_csv_upload(request):
    """
    Handles the batch upload of volunteers from a CSV file.
    - On GET, it displays the CSV upload form.
    - On POST, it processes the uploaded CSV file, parses it, and uses the
      HubspotAPI service to create the contacts in HubSpot in a batch.
      It then displays a success page with the results of the import.

    Template: 'volunteer/volunteer_csv_upload.html'
    Success Template: 'volunteer/csv_upload_success.html'
    """
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            # Read and decode the uploaded file
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            # Use DictReader to parse the CSV into a list of dictionaries
            reader = csv.DictReader(io_string)

            contacts_to_create = []
            for row in reader:
                # Map CSV columns to HubSpot properties
                contacts_to_create.append({
                    "email": row.get('email'),
                    "firstname": row.get('name'),
                    "phone": row.get('phone_number'),
                    "preferred_volunteer_role": row.get('preferred_volunteer_role'),
                    "availability": row.get('availability'),
                    "how_did_you_hear_about_us": row.get('how_did_you_hear_about_us'),
                })

            if contacts_to_create:
                hubspot_api = HubspotAPI()
                # Call the batch create method
                api_response = hubspot_api.batch_create_contacts(contacts_to_create)
                # Render a success page with the API response
                return render(request, 'volunteer/csv_upload_success.html', {'response': api_response})

    else:
        form = CSVUploadForm()
    return render(request, 'volunteer/volunteer_csv_upload.html', {'form': form})

def volunteer_update(request, contact_id):
    """
    Handles the editing of an existing volunteer.
    - On GET, it fetches the contact's data from HubSpot and displays it in a
      pre-filled form.
    - On POST, it validates the submitted data and, if valid, updates the
      contact in HubSpot.

    Template: 'volunteer/volunteer_update.html'
    """
    hubspot_api = HubspotAPI()
    contact = hubspot_api.get_contact(contact_id)
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            # Prepare the properties for the HubSpot API
            properties = {
                "email": form.cleaned_data['email'],
                "firstname": form.cleaned_data['name'],
                "phone": form.cleaned_data['phone_number'],
                "preferred_volunteer_role": form.cleaned_data['preferred_volunteer_role'],
                "availability": form.cleaned_data['availability'],
                "how_did_you_hear_about_us": form.cleaned_data['how_did_you_hear_about_us'],
            }
            # Update the contact in HubSpot
            hubspot_api.update_contact(contact_id, properties)
            # Redirect to the detail page for the updated contact
            return redirect('volunteer_detail', contact_id=contact_id)
    else:
        # Pre-fill the form with the contact's existing data
        initial_data = {
            'name': contact.properties.get('firstname', ''),
            'email': contact.properties.get('email', ''),
            'phone_number': contact.properties.get('phone', ''),
            'preferred_volunteer_role': contact.properties.get('preferred_volunteer_role', ''),
            'availability': contact.properties.get('availability', ''),
            'how_did_you_hear_about_us': contact.properties.get('how_did_you_hear_about_us', ''),
        }
        form = VolunteerForm(initial=initial_data)
    return render(request, 'volunteer/volunteer_update.html', {'form': form, 'contact_id': contact_id})

def volunteer_delete(request, contact_id):
    """
    Handles the deletion of a volunteer.
    - On GET, it displays a confirmation page.
    - On POST, it deletes the contact from HubSpot and also from the local
      database if it exists.

    Template: 'volunteer/volunteer_delete_confirm.html'
    """
    hubspot_api = HubspotAPI()
    contact = hubspot_api.get_contact(contact_id)
    if request.method == 'POST':
        # Delete from HubSpot
        hubspot_api.delete_contact(contact_id)

        # Also delete from the local database
        try:
            # Find the local volunteer by their email address
            local_volunteer = Volunteer.objects.get(email=contact.properties.get('email'))
            local_volunteer.delete()
        except Volunteer.DoesNotExist:
            # If the contact is not in the local DB, we can ignore it
            pass

        # Redirect to the volunteer list after deletion
        return redirect('volunteer_list')

    # On GET, show the confirmation page
    return render(request, 'volunteer/volunteer_delete_confirm.html', {'contact': contact})
