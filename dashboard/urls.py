from django.urls import path
from .views import *
from .api_view import *
app_name = 'dashboard'

urlpatterns = [
          path('',DoctorDashBoard.as_view(),name='dashboard'),
          path('update-doctorprfile/',DoctorProfileUpdateView.as_view(),name='update'),
          path('approve/<int:id>/',approve_appointment,name='approve'),
          path('delete-reservation/<int:pk>/',DeleteReservation.as_view(),name='delete'),
          path('patient-profile/<int:pk>/',PatientProfileDashboard.as_view(),name='appointment-detail'),
          path('schedule-appointment/<int:pk>/',ScheduleAppointment.as_view(),name='schedule'),
          path("report/", generate_report_patient, name="generate_report"),
          # API
          # Doctor Dashboard
          path('api/doctors/<int:id>/dashboard/', UpdateDoctorDashboardAPIView.as_view(), name='doctor-dashboard-update'),

          # Appointments
          path('api/appointments/<int:pk>/', DeleteAppointment.as_view(), name='appointment-delete'),
          path('api/appointments/', AppointmentListAPIView.as_view(), name='appointment-list'),
          path('api/appointments/<int:id>/approve/', approve_appointment, name='appointment-approve'),
          path('api/appointments/<int:pk>/schedule/', ScheduleAppointmentAPIView.as_view(), name='appointment-schedule'),

          # Patient Profile
          path('api/patients/<int:id>/dashboard/', ViewProfilePatientAPIView.as_view(), name='patient-dashboard-view'),


]