"""
This file contains the view functions for the volunteer application, primarily for
rendering HTML templates. These views handle the traditional, server-rendered parts
of the site.

Views are responsible for handling web requests and returning web responses.
They contain application logic, interacting with the database (via models)
and rendering templates.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import VolunteerForm, CSVUploadForm
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
      it saves the new volunteer to the local database with a 'pending' status
      and then redirects to a success page.
    """
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = VolunteerForm()
    return render(request, 'volunteer/signup.html', {'form': form})

def success(request):
    """
    Displays a simple success page after a volunteer successfully signs up.
    """
    return render(request, 'volunteer/success.html')

@login_required
def volunteer_list(request):
    """
    Displays a list of all volunteers from the local database.
    If a search query is provided, it filters volunteers by first or last name.
    """
    query = request.GET.get('q')
    if query:
        contacts = Volunteer.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    else:
        contacts = Volunteer.objects.all()

    return render(request, 'volunteer/volunteer_list.html', {'contacts': contacts, 'query': query})

@login_required
def volunteer_detail(request, volunteer_id):
    """
    Displays the details of a single volunteer from the local database.
    """
    volunteer = get_object_or_404(Volunteer, pk=volunteer_id)
    return render(request, 'volunteer/volunteer_detail.html', {'volunteer': volunteer})

@login_required
def volunteer_csv_upload(request):
    """
    Handles the batch upload of volunteers from a CSV file.

    On POST, it processes the uploaded CSV, creates new Volunteer records
    in the database with a 'pending' status, and displays the results.
    """
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)

            volunteers_created = 0
            errors = []
            for row in reader:
                try:
                    Volunteer.objects.create(
                        first_name=row.get('first_name', ''),
                        last_name=row.get('last_name', ''),
                        email=row.get('email'),
                        phone_number=row.get('phone_number'),
                        preferred_volunteer_role=row.get('preferred_volunteer_role'),
                        availability=row.get('availability'),
                        how_did_you_hear_about_us=row.get('how_did_you_hear_about_us'),
                    )
                    volunteers_created += 1
                except Exception as e:
                    errors.append(f"Could not create volunteer from row: {row}. Error: {e}")

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
    Handles the editing of an existing volunteer's details.
    """
    volunteer = get_object_or_404(Volunteer, pk=volunteer_id)
    if request.method == 'POST':
        form = VolunteerForm(request.POST, instance=volunteer)
        if form.is_valid():
            form.save()
            return redirect('volunteer_detail', volunteer_id=volunteer.id)
    else:
        form = VolunteerForm(instance=volunteer)
    return render(request, 'volunteer/volunteer_update.html', {'form': form, 'volunteer': volunteer})

@login_required
def volunteer_delete(request, volunteer_id):
    """
    Handles the deletion of a volunteer from the local database.
    """
    volunteer = get_object_or_404(Volunteer, pk=volunteer_id)
    if request.method == 'POST':
        volunteer.delete()
        return redirect('volunteer_list')
    return render(request, 'volunteer/volunteer_delete_confirm.html', {'volunteer': volunteer})

@login_required
def volunteer_approve(request, volunteer_id):
    """
    Approves a volunteer application. This view is now primarily for
    demonstration in a template-based flow. The core approval logic
    is handled by the API view in `api_views.py`.
    """
    if request.method == 'POST':
        volunteer = get_object_or_404(Volunteer, pk=volunteer_id)
        if volunteer.status == 'pending':
            volunteer.status = 'approved'
            volunteer.save()
        return redirect('volunteer_list')
    return redirect('volunteer_list')

@login_required
def volunteer_reject(request, volunteer_id):
    """
    Rejects a volunteer application.
    """
    if request.method == 'POST':
        volunteer = get_object_or_404(Volunteer, pk=volunteer_id)
        volunteer.status = 'rejected'
        volunteer.save()
        return redirect('volunteer_list')
    return redirect('volunteer_list')
