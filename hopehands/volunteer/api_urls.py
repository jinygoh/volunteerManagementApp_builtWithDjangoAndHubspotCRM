from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views
from django.views.decorators.csrf import csrf_exempt

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'volunteers', api_views.VolunteerViewSet, basename='volunteer')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('login/', api_views.LoginView.as_view(), name='api-login'),
    path('logout/', api_views.LogoutView.as_view(), name='api-logout'),
    path('signup/', csrf_exempt(api_views.VolunteerPublicCreateView.as_view()), name='volunteer-signup-api'),
    path('', include(router.urls)),
]
