from django.urls import path
from .views import *
app_name = 'dashboard'

urlpatterns = [
          path('',DoctorDashBoard.as_view(),name='dashboard'),
          path('update-doctorprfile/',DoctorProfileUpdateView.as_view(),name='update'),
          path('approve/<int:id>/',approve_appointment,name='approve'),
          path('delete-reservation/<int:pk>/',DeleteReservation.as_view(),name='delete'),
          path('patient-profile/<int:pk>/',PatientProfileDashboard.as_view(),name='appointment-detail')
          
]