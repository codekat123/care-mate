from django.urls import path
from .views import *

app_name = 'profile'

urlpatterns = [
     path('profile_doctor/',ProfileDoctor.as_view(),name='profile_doctor'),
     path('profile_patient/',ProfilePatient.as_view(),name='profile_patient'),
     path('edit_doctor/',DoctorProfileUpdateView.as_view(),name='edit_doctor'),
     path('edit_patient/',PatientProfileUpdateView.as_view(),name='edit_patient'),
]