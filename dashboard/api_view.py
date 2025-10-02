from rest_framework.generics import RetrieveAPIView , UpdateAPIView , ListAPIView , DestroyAPIView 
from rest_framework.permissions import AllowAny , IsAuthenticated
from profile_users.models import DoctorProfile , PatientProfile
from .serializer import DoctorDashBoardSerializer
from rest_framework.exceptions import NotFound
from home.models import Reservation
from profile_users.serializer import ReservationSerializer
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from rest_framework.throttling import UserRateThrottle

class UpdateDoctorDashboardAPIView(UpdateAPIView):
     queryset = DoctorProfile.objects.all()
     serializer_class = DoctorDashBoardSerializer
     throttle_classes = [UserRateThrottle]

     def get_object(self):
          try:
               return DoctorProfile.objects.get(user=self.request.user)
          except DoctorProfile.DoesNotExist:
               return NotFound("profile not found")
          

class ViewProfilePatientAPIView(RetrieveAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorDashBoardSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_object(self):
        id = self.kwargs.get('id')
        user = get_object_or_404(PatientProfile,id=id)
        if not user or user.is_anonymous:
            raise NotFound("User not authenticated")

        try:
            return DoctorProfile.objects.get(user=user)
        except DoctorProfile.DoesNotExist:
            raise NotFound("Profile not found")
 

class AppointmentListAPIView(ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        user = self.request.user
        if not user or user.is_anonymous:
            raise NotFound("User not authenticated")

        try:
                return Reservation.objects.filter(doctor=self.request.user.doctor)
        except Reservation.DoesNotExist:
            raise NotFound("Profile not found")
        
class DeleteAppointment(DestroyAPIView):
     queryset = Reservation.objects.all()
     serializer_class = ReservationSerializer
     permission_classes = [IsAuthenticated]
     throttle_classes = [UserRateThrottle]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_appointment(request, id):
    appointment = get_object_or_404(Reservation, id=id)

    appointment.is_approved = not appointment.is_approved
    appointment.save()

    return Response(
        {"is_approved": appointment.is_approved},
        status=status.HTTP_200_OK
    )

class ScheduleAppointmentAPIView(UpdateAPIView):
     queryset = Reservation.objects.all()
     serializer_class = ReservationSerializer
     throttle_classes = [UserRateThrottle]
