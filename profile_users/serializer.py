from rest_framework import serializers
from .models import PatientProfile , DoctorProfile 
from home.models import Reservation

class PatientProfileSerializer(serializers.ModelSerializer):
     class Meta:
          model = PatientProfile
          fields = '__all__'
class ReservationSerializer(serializers.ModelSerializer):
     class Meta:
          model = Reservation
          fields = '__all__'
          