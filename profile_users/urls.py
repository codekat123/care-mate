from django.urls import path
from .views import *
from .api_view import *
app_name = 'profile'

urlpatterns = [
     path('profile_patient/',ProfilePatient.as_view(),name='profile_patient'),
     path('edit_patient/',PatientProfileUpdateView.as_view(),name='edit_patient'),
     path('view-appointments/',ShowAppointment.as_view(),name='view_appointments'),
     path('rating-doctor/<int:doctor_id>/',rate_doctor,name='rate'),
               # API 
     path('api/update/profile_patient/',ProfilePatientUpdateAPIView.as_view(),name='edit_patient'),
     path('api/profile_patient/',ProfilePatientAPIView.as_view(),name='profile_patient'),
]