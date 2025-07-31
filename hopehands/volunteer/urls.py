# Import the path function from Django's URL library.
from django.urls import path
# Import the views from the current app (volunteer).
from . import views

# The `urlpatterns` list defines the URL patterns for the volunteer app.
# These patterns are included in the main `urls.py` file under the 'volunteer/' prefix.
urlpatterns = [
    # This pattern maps the 'volunteer/signup/' URL to the `volunteer_signup` view.
    # The `name='signup'` argument allows this URL to be referenced by name.
    path('signup/', views.volunteer_signup, name='signup'),

    # This pattern maps the 'volunteer/success/' URL to the `success` view.
    # This page is shown after a volunteer successfully signs up.
    path('success/', views.success, name='success'),
]
