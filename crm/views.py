from django.shortcuts import render, redirect
from .forms import VolunteerForm
from django.conf import settings
from hubspot import HubSpot

def register_volunteer(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            volunteer = form.save(commit=False)
            volunteer.approved = True  # Auto-approve for now
            volunteer.save()

            if volunteer.approved:
                try:
                    hubspot = HubSpot(api_key=settings.HUBSPOT_API_KEY)
                    properties = {
                        "email": volunteer.email,
                        "firstname": volunteer.first_name,
                        "lastname": volunteer.last_name,
                        "phone": volunteer.phone,
                    }
                    simple_public_object_input = {
                        "properties": properties
                    }
                    api_response = hubspot.crm.contacts.basic_api.create(
                        simple_public_object_input=simple_public_object_input
                    )
                except Exception as e:
                    # Handle HubSpot API errors
                    print(f"Error creating HubSpot contact: {e}")

            return redirect('success')
    else:
        form = VolunteerForm()
    return render(request, 'crm/register.html', {'form': form})

from .models import Volunteer

def registration_success(request):
    return render(request, 'crm/success.html')

def volunteer_list(request):
    volunteers = Volunteer.objects.all()
    return render(request, 'crm/volunteer_list.html', {'volunteers': volunteers})

def volunteer_update(request, pk):
    volunteer = Volunteer.objects.get(pk=pk)
    if request.method == 'POST':
        form = VolunteerForm(request.POST, instance=volunteer)
        if form.is_valid():
            form.save()
            return redirect('volunteer_list')
    else:
        form = VolunteerForm(instance=volunteer)
    return render(request, 'crm/register.html', {'form': form})

import csv
from django.shortcuts import render, redirect
from .forms import VolunteerForm
from .models import Volunteer

def volunteer_delete(request, pk):
    volunteer = Volunteer.objects.get(pk=pk)
    if request.method == 'POST':
        volunteer.delete()
        return redirect('volunteer_list')
    return render(request, 'crm/volunteer_confirm_delete.html', {'volunteer': volunteer})

import matplotlib.pyplot as plt
import io
import base64
from django.http import HttpResponse

def import_volunteers(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            Volunteer.objects.create(
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                phone=row['phone'],
                address=row['address'],
                skills=row['skills'],
                approved=row.get('approved', False)
            )
        return redirect('volunteer_list')
    return render(request, 'crm/import_volunteers.html')

def skills_chart(request):
    skills_data = {}
    volunteers = Volunteer.objects.all()
    for volunteer in volunteers:
        skills = [s.strip() for s in volunteer.skills.split(',')]
        for skill in skills:
            if skill:
                skills_data[skill] = skills_data.get(skill, 0) + 1

    fig, ax = plt.subplots()
    ax.bar(skills_data.keys(), skills_data.values())
    ax.set_ylabel('Number of Volunteers')
    ax.set_title('Volunteers by Skill')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + string.decode('utf-8')

    return render(request, 'crm/skills_chart.html', {'chart': uri})
