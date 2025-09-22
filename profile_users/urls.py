from django.urls import path
from .views import *

app_name = 'profile'

urlpatterns = [
     path('profile_patient/',ProfilePatient.as_view(),name='profile_patient'),
     path('edit_patient/',PatientProfileUpdateView.as_view(),name='edit_patient'),
     path('view-appointments/',ShowAppointment.as_view(),name='view_appointments')
]