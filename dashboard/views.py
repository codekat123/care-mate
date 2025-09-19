from django.shortcuts import render
from profile_users.models import DoctorProfile
from django.views.generic import DetailView




class DoctorDashBoard(DetailView):
     model = DoctorProfile
     template_name = 'dashboard/dashboard_doctor'

     def get_object(self,queryset=None):
          return DoctorProfile.objects.get(user=self.request.user)
     