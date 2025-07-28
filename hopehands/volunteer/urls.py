from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.volunteer_signup, name='signup'),
    path('success/', views.success, name='success'),
]
