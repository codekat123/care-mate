from rest_framework.generics import ListAPIView , CreateAPIView , RetrieveAPIView
from restframework.permissions import IsAuthenticated , AllowAny
from profile_users.models import DoctorProfile
from dashboard.serializer import DoctorDashBoardSerializer
from rest_framework.filters import SearchFilter

class ListHome(ListAPIView):
     queryset = DoctorProfile.objects.all()
     serializer_class = DoctorDashBoardSerializer
     permission_classes = [IsAuthenticated]
     filter_backends = [SearchFilter]
     search_fields = ['first_name','major'] 

     def get_queryset(self):
          return DoctorProfile.objects.filter(is_active=True)

class DetailHome(RetrieveAPIView):
     queryset = DoctorProfile.objects.all()
     serializer_class = DoctorDashBoardSerializer
     permission_classes = [IsAuthenticated]
     