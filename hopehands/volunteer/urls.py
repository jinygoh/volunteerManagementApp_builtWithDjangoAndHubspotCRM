# hopehands/volunteer/urls.py

"""
This file defines the URL patterns for the volunteer application.
URL patterns map URLs (as strings) to view functions in `views.py`. When a user
requests a URL, Django goes through each pattern in order and stops at the first
one that matches the requested URL.

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.urls import path
from . import views

# A list of URL patterns for the volunteer app.
urlpatterns = [
    # URL for the volunteer signup page.
    path('signup/', views.volunteer_signup, name='signup'),
    # URL for the success page, shown after a successful signup.
    path('success/', views.success, name='success'),
    # URL for the list of all volunteers.
    path('list/', views.volunteer_list, name='volunteer_list'),
    # URL for viewing the details of a single volunteer.
    path('volunteer/<int:volunteer_id>/', views.volunteer_detail, name='volunteer_detail'),
    # URL for updating an existing volunteer.
    path('volunteer/<int:volunteer_id>/update/', views.volunteer_update, name='volunteer_update'),
    # URL for deleting an existing volunteer.
    path('volunteer/<int:volunteer_id>/delete/', views.volunteer_delete, name='volunteer_delete'),
    # URL for approving a volunteer application.
    path('volunteer/<int:volunteer_id>/approve/', views.volunteer_approve, name='volunteer_approve'),
    # URL for rejecting a volunteer application.
    path('volunteer/<int:volunteer_id>/reject/', views.volunteer_reject, name='volunteer_reject'),
    # URL for the CSV upload page.
    path('upload-csv/', views.volunteer_csv_upload, name='volunteer_csv_upload'),
]
