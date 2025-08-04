from django.shortcuts import render, redirect
from .forms import VolunteerForm
from .hubspot_api import HubspotAPI
import logging

logger = logging.getLogger(__name__)

def volunteer_signup(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            volunteer = form.save()
            hubspot_api = HubspotAPI()
            hubspot_api.create_contact(
                email=volunteer.email,
                name=volunteer.name,
                phone_number=volunteer.phone_number,
                preferred_volunteer_role=volunteer.preferred_volunteer_role,
                availability=volunteer.availability,
                how_did_you_hear_about_us=volunteer.how_did_you_hear_about_us,
            )
            return redirect('success')
    else:
        form = VolunteerForm()
    return render(request, 'volunteer/signup.html', {'form': form})

def success(request):
    return render(request, 'volunteer/success.html')

def volunteer_list(request):
    hubspot_api = HubspotAPI()
    contacts = hubspot_api.get_all_contacts()
    return render(request, 'volunteer/volunteer_list.html', {'contacts': contacts})

def volunteer_detail(request, contact_id):
    hubspot_api = HubspotAPI()
    contact = hubspot_api.get_contact(contact_id)
    return render(request, 'volunteer/volunteer_detail.html', {'contact': contact})

from .models import Volunteer
from .forms import CSVUploadForm
import csv
import io

def volunteer_csv_upload(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)

            contacts_to_create = []
            for row in reader:
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
                api_response = hubspot_api.batch_create_contacts(contacts_to_create)
                # You can add more detailed feedback based on the api_response
                return render(request, 'volunteer/csv_upload_success.html', {'response': api_response})

    else:
        form = CSVUploadForm()
    return render(request, 'volunteer/volunteer_csv_upload.html', {'form': form})

def volunteer_update(request, contact_id):
    hubspot_api = HubspotAPI()
    contact = hubspot_api.get_contact(contact_id)
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            properties = {
                "email": form.cleaned_data['email'],
                "firstname": form.cleaned_data['name'],
                "phone": form.cleaned_data['phone_number'],
                "preferred_volunteer_role": form.cleaned_data['preferred_volunteer_role'],
                "availability": form.cleaned_data['availability'],
                "how_did_you_hear_about_us": form.cleaned_data['how_did_you_hear_about_us'],
            }
            hubspot_api.update_.contact(contact_id, properties)
            return redirect('volunteer_detail', contact_id=contact_id)
    else:
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
    hubspot_api = HubspotAPI()
    contact = hubspot_api.get_contact(contact_id)
    if request.method == 'POST':
        # Delete from HubSpot
        hubspot_api.delete_contact(contact_id)

        # Delete from local database
        try:
            local_volunteer = Volunteer.objects.get(email=contact.properties.get('email'))
            local_volunteer.delete()
        except Volunteer.DoesNotExist:
            pass # Contact was not in the local DB

        return redirect('volunteer_list')

    return render(request, 'volunteer/volunteer_delete_confirm.html', {'contact': contact})
