from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'volunteers', api_views.VolunteerViewSet, basename='volunteer')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('login/', api_views.LoginView.as_view(), name='api-login'),
    path('signup/', api_views.VolunteerPublicCreateView.as_view(), name='volunteer-signup-api'),
    path('', include(router.urls)),
]
