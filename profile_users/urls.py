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
     # Patients
     path('api/patients/', ProfilePatientUpdateAPIView.as_view(), name='patient-update'),
     path('api/patients/', ProfilePatientAPIView.as_view(), name='patient-detail'),
     
     # Appointments
     path('api/appointments/', AppointmentListAPIView.as_view(), name='appointment-list'),

]