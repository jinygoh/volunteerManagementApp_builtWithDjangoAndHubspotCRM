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
from django.contrib.auth.decorators import login_required
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
            # Save the new volunteer to the local database. The status will default to 'pending'.
            form.save()
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

@login_required
def volunteer_list(request):
    """
    Displays a list of all volunteers from the local database.
    If a search query is provided in the GET request, it filters volunteers by name.

    Template: 'volunteer/volunteer_list.html'
    """
    query = request.GET.get('q')
    if query:
        # If there is a query, search for local volunteers
        contacts = Volunteer.objects.filter(name__icontains=query)
    else:
        # Otherwise, get all local volunteers
        contacts = Volunteer.objects.all()

    return render(request, 'volunteer/volunteer_list.html', {'contacts': contacts, 'query': query})

@login_required
def volunteer_detail(request, volunteer_id):
    """
    Displays the details of a single volunteer from the local database.
    It takes a volunteer_id, fetches the corresponding Volunteer object,
    and displays its details.

    Template: 'volunteer/volunteer_detail.html'
    """
    volunteer = get_object_or_404(Volunteer, pk=volunteer_id)
    return render(request, 'volunteer/volunteer_detail.html', {'volunteer': volunteer})

@login_required
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

            volunteers_created = 0
            errors = []
            for row in reader:
                try:
                    Volunteer.objects.create(
                        name=row.get('name'),
                        email=row.get('email'),
                        phone_number=row.get('phone_number'),
                        preferred_volunteer_role=row.get('preferred_volunteer_role'),
                        availability=row.get('availability'),
                        how_did_you_hear_about_us=row.get('how_did_you_hear_about_us'),
                        # Status will default to 'pending'
                    )
                    volunteers_created += 1
                except Exception as e:
                    errors.append(f"Could not create volunteer from row: {row}. Error: {e}")

            # Render a success page with the results
            return render(request, 'volunteer/csv_upload_success.html', {
                'volunteers_created': volunteers_created,
                'errors': errors
            })

    else:
        form = CSVUploadForm()
    return render(request, 'volunteer/volunteer_csv_upload.html', {'form': form})

@login_required
def volunteer_update(request, volunteer_id):
    """
    Handles the editing of an existing volunteer from the local database.
    - On GET, it displays the volunteer's data in a form.
    - On POST, it updates the volunteer's data in the local database.
    If the volunteer is already approved, it also updates the contact in HubSpot.

    Template: 'volunteer/volunteer_update.html'
    """
    volunteer = get_object_or_404(Volunteer, pk=volunteer_id)
    if request.method == 'POST':
        form = VolunteerForm(request.POST, instance=volunteer)
        if form.is_valid():
            updated_volunteer = form.save()

            # If the volunteer is approved and has a HubSpot ID, update their HubSpot contact.
            if updated_volunteer.status == 'approved' and updated_volunteer.hubspot_id:
                hubspot_api = HubspotAPI()
                properties = {
                    "email": updated_volunteer.email,
                    "firstname": updated_volunteer.name,
                    "phone": updated_volunteer.phone_number,
                    "preferred_volunteer_role": updated_volunteer.preferred_volunteer_role,
                    "availability": updated_volunteer.availability,
                    "how_did_you_hear_about_us": updated_volunteer.how_did_you_hear_about_us,
                }
                hubspot_api.update_contact(updated_volunteer.hubspot_id, properties)

            return redirect('volunteer_detail', volunteer_id=volunteer.id)
    else:
        form = VolunteerForm(instance=volunteer)
    return render(request, 'volunteer/volunteer_update.html', {'form': form, 'volunteer': volunteer})

@login_required
def volunteer_delete(request, volunteer_id):
    """
    Handles the deletion of a volunteer from the local database.
    - On GET, it displays a confirmation page.
    - On POST, it deletes the volunteer from the local database.

    Template: 'volunteer/volunteer_delete_confirm.html'
    """
    volunteer = get_object_or_404(Volunteer, pk=volunteer_id)
    if request.method == 'POST':
        volunteer.delete()
        return redirect('volunteer_list')
    return render(request, 'volunteer/volunteer_delete_confirm.html', {'volunteer': volunteer})

@login_required
def volunteer_approve(request, volunteer_id):
    """
    Approves a volunteer application.
    This view changes the volunteer's status to 'approved' and creates a
    corresponding contact in HubSpot.
    """
    if request.method == 'POST':
        volunteer = get_object_or_404(Volunteer, pk=volunteer_id)
        volunteer.status = 'approved'
        volunteer.save()

        # Create the contact in HubSpot
        hubspot_api = HubspotAPI()
        api_response = hubspot_api.create_contact(
            email=volunteer.email,
            name=volunteer.name,
            phone_number=volunteer.phone_number,
            preferred_volunteer_role=volunteer.preferred_volunteer_role,
            availability=volunteer.availability,
            how_did_you_hear_about_us=volunteer.how_did_you_hear_about_us,
        )
        # Save the HubSpot ID to the local volunteer record
        if api_response:
            volunteer.hubspot_id = api_response.id
            volunteer.save()

        return redirect('volunteer_list')
    return redirect('volunteer_list')

@login_required
def volunteer_reject(request, volunteer_id):
    """
    Rejects a volunteer application.
    This view changes the volunteer's status to 'rejected'.
    """
    if request.method == 'POST':
        volunteer = get_object_or_404(Volunteer, pk=volunteer_id)
        volunteer.status = 'rejected'
        volunteer.save()
        return redirect('volunteer_list')
    return redirect('volunteer_list')
