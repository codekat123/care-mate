from rest_framework.generics import UpdateAPIView , RetrieveAPIView , ListAPIView
from .models import PatientProfile
from home.models import Reservation
from .serializer import PatientProfileSerializer , ReservationSerializer
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated 

class ProfilePatientUpdateAPIView(UpdateAPIView):
     queryset = PatientProfile.objects.all()
     serializer_class = PatientProfileSerializer
     permission_classes = [IsAuthenticated]

     def get_object(self):
          try:
               return PatientProfile.objects.get(user=self.request.user)
          except PatientProfile.DoesNotExist:
               raise NotFound("Profile not found")


class ProfilePatientAPIView(RetrieveAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if not user or user.is_anonymous:
            raise NotFound("User not authenticated")

        try:
            return PatientProfile.objects.get(user=user)
        except PatientProfile.DoesNotExist:
            raise NotFound("Profile not found")
 

class AppointmentListAPIView(ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user or user.is_anonymous:
            raise NotFound("User not authenticated")

        try:
                return Reservation.objects.filter(patient=self.request.user.patient)
        except Reservation.DoesNotExist:
            raise NotFound("Profile not found")

