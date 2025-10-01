from rest_framework import serializers
from profile_users.models import DoctorProfile

class DoctorDashBoardSerializer(serializers.ModelSerializer):
     class Meta:
          model = DoctorProfile
          fields = '__all__'
          