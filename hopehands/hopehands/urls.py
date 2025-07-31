# Import necessary functions from Django.
from django.contrib import admin  # For the admin site.
from django.urls import path, include  # For defining URL patterns and including other URLconfs.
# Import the views from the volunteer app to reference them in the URL patterns.
from volunteer import views as volunteer_views

# The `urlpatterns` list routes URLs to views.
# Django checks each URL pattern in order, from top to bottom.
urlpatterns = [
    # The URL for the Django admin interface.
    path("admin/", admin.site.urls),

    # The root URL of the site.
    # This pattern maps the root URL ('') to the `volunteer_signup` view.
    # The `name='home'` argument gives this URL a name, which can be used to refer to it in templates and other parts of the app.
    path("", volunteer_views.volunteer_signup, name="home"),

    # This pattern includes the URL patterns from the `volunteer` app.
    # Any URL that starts with 'volunteer/' will be handled by the `volunteer/urls.py` file.
    path('volunteer/', include('volunteer.urls')),
]
