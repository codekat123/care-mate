from rest_framework.generics import ListAPIView , CreateAPIView , RetrieveAPIView
from rest_framework.permissions import IsAuthenticated , AllowAny
from profile_users.models import DoctorProfile
from dashboard.serializer import DoctorDashBoardSerializer
from rest_framework.filters import SearchFilter
from rest_framework.throttling import UserRateThrottle

class ListHome(ListAPIView):
     queryset = DoctorProfile.objects.all()
     serializer_class = DoctorDashBoardSerializer
     permission_classes = [IsAuthenticated]
     throttle_classes = [UserRateThrottle]
     filter_backends = [SearchFilter]
     search_fields = ['first_name','major'] 

     def get_queryset(self):
          return DoctorProfile.objects.filter(is_active=True)

class DetailHome(RetrieveAPIView):
     queryset = DoctorProfile.objects.all()
     serializer_class = DoctorDashBoardSerializer
     permission_classes = [IsAuthenticated]
     throttle_classes = [UserRateThrottle]
     