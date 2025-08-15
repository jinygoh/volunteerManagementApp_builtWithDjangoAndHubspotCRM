from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'volunteers', api_views.VolunteerViewSet, basename='volunteer')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', api_views.VolunteerPublicCreateView.as_view(), name='volunteer-signup-api'),
    path('upload-csv/', api_views.VolunteerCSVUploadAPIView.as_view(), name='upload-csv'),
    path('', include(router.urls)),
]
