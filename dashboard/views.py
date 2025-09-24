from django.shortcuts import render , redirect
from profile_users.models import DoctorProfile , PatientProfile
from django.views.generic import DetailView , DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from profile_users.views import BaseProfileUpdateView
from django.urls import reverse_lazy
from profile_users.forms import UserForm , DoctorProfileForm
from home.models import Reservation
from django.views.generic.edit import UpdateView
from django.views.decorators.http import require_POST
from datetime import date
from chat.models import Message




@method_decorator(login_required(login_url='user_account:login'),name='dispatch')
class DoctorDashBoard(DetailView):
     model = DoctorProfile
     template_name = 'dashboard/dashbaord_doctor.html'
     context_object_name = 'doctor_Profile'

     def get_object(self,queryset=None):
          return DoctorProfile.objects.get(user=self.request.user)
     
     
     def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['appointments'] = Reservation.objects.filter(doctor=self.request.user.doctor)
         context['count_of_reservation'] = Reservation.objects.filter(doctor=self.request.user.doctor).count()
         context['doctor_Profile'] = self.object
         context['count_of_notifications'] = Message.objects.filter(sender=self.request.user).count()
         context['notifications'] = Message.objects.filter(sender=self.request.user).order_by('-created_at')[:7]
         return context


@method_decorator(login_required(login_url='user_account:login'),name='dispatch')
class DoctorProfileUpdateView(BaseProfileUpdateView):
    user_form_class = UserForm
    form_class = DoctorProfileForm
    template_name = 'dashboard/edit_doctor.html'
    model_field = 'doctor'
    success_url = reverse_lazy('dashboard:dashboard')

class DeleteReservation(DeleteView):
     model = Reservation
     template_name = 'dashboard/comfirmation_delete_reservation.html'
     success_url = reverse_lazy('dashboard:dashboard')

@require_POST
def approve_appointment(request,id):
     approve =  Reservation.objects.get(id=id)
     if not approve.is_approved:
          approve.is_approved = True
     else:
          approve.is_approved = False
     approve.save()
     return redirect('/')

@method_decorator(login_required(login_url='user_account:login'),name='dispatch')
class PatientProfileDashboard(DetailView):
     model = PatientProfile
     template_name = 'profile/profile_patient.html'
     
     @staticmethod
     def calculate_age(birthday):
          today = date.today()
          age = today.year - birthday.year - (
        (today.month, today.day) < (birthday.month, birthday.day)
               )
          return age

     def get_context_data(self,**kwargs):
          context = super().get_context_data(**kwargs)
          id = self.kwargs['pk']
          patient = PatientProfile.objects.get(id=id)
          context['patient'] = patient
          context['age'] = self.calculate_age(patient.date_of_birthday)
          return context

@method_decorator(login_required(login_url='user_account:login'),name='dispatch')
class ScheduleAppointment(UpdateView):
     model = Reservation
     fields = ['appointment']
     template_name = 'dashboard/dashboard_doctor.html'
     success_url = reverse_lazy("dashboard:dashboard")