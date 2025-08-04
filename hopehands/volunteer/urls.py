from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.volunteer_signup, name='signup'),
    path('success/', views.success, name='success'),
    path('list/', views.volunteer_list, name='volunteer_list'),
    path('contact/<int:contact_id>/', views.volunteer_detail, name='volunteer_detail'),
    path('contact/<int:contact_id>/update/', views.volunteer_update, name='volunteer_update'),
    path('contact/<int:contact_id>/delete/', views.volunteer_delete, name='volunteer_delete'),
    path('upload-csv/', views.volunteer_csv_upload, name='volunteer_csv_upload'),
]
