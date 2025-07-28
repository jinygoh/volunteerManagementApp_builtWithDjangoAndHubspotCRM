from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_volunteer, name='register'),
    path('success/', views.registration_success, name='success'),
    path('', views.volunteer_list, name='volunteer_list'),
    path('update/<int:pk>/', views.volunteer_update, name='volunteer_update'),
    path('delete/<int:pk>/', views.volunteer_delete, name='volunteer_delete'),
    path('import/', views.import_volunteers, name='import_volunteers'),
    path('skills-chart/', views.skills_chart, name='skills_chart'),
    path('pending/', views.pending_volunteers, name='pending_volunteers'),
    path('approve/<int:pk>/', views.approve_volunteer, name='approve_volunteer'),
    path('reject/<int:pk>/', views.reject_volunteer, name='reject_volunteer'),
]
