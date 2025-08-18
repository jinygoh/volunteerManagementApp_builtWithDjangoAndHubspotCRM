"""
Main URL configuration for the HopeHands project.

This file routes URLs to the appropriate Django apps or views. It serves as the
primary URL dispatcher for the entire application.

The URL patterns include:
- The Django admin site.
- Authentication views (login/logout) for the template-based admin.
- The REST API endpoints, which are delegated to the `volunteer.api_urls` module.
- The main application URLs, which are delegated to the `volunteer.urls` module.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from volunteer import views as volunteer_views

urlpatterns = [
    # Admin site for database management.
    path("admin/", admin.site.urls),

    # Authentication views for the server-rendered parts of the site.
    path("accounts/login/", auth_views.LoginView.as_view(template_name="volunteer/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),

    # Include all API endpoints under the '/api/' prefix.
    path('api/', include('volunteer.api_urls')),

    # The root path ("/") is set as the homepage, which shows the volunteer list.
    path("", volunteer_views.volunteer_list, name="home"),
    # Include all other volunteer app URLs (for templates).
    path('volunteer/', include('volunteer.urls')),
]
