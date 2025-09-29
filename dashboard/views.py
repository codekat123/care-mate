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
from .forms import PatientReport
from django.db.models import Q
from django.http import HttpResponse
import csv
import datetime
from django.core.paginator import Paginator

@method_decorator(login_required(login_url='user_account:login'),name='dispatch')
class DoctorDashBoard(DetailView):
     model = DoctorProfile
     template_name = 'dashboard/dashbaord_doctor.html'
     context_object_name = 'doctor_Profile'

     def get_object(self,queryset=None):
          return DoctorProfile.objects.get(user=self.request.user)
     
     
     def get_context_data(self, **kwargs):
         

         appointments = Reservation.objects.filter(doctor=self.request.user.doctor)
         paginator = Paginator(appointments, 10)  
         page_number = self.request.GET.get("page")
         page_obj = paginator.get_page(page_number)

         context = super().get_context_data(**kwargs)
         context['appointments'] = page_obj
         context['count_of_reservation'] = Reservation.objects.filter(doctor=self.request.user.doctor).count()
         context['doctor_Profile'] = self.object
         context['count_of_notifications'] = Message.objects.filter(sender=self.request.user).count()
         context['notifications'] = Message.objects.filter(sender=self.request.user).order_by('-created_at')[:7]
         context['patient_report'] = PatientReport()
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



@login_required(login_url="user_account:login")
@require_POST
def generate_report_patient(request):
    form = PatientReport(request.POST)
    if not form.is_valid():
        return HttpResponse("Invalid input", status=400)

    start_date = form.cleaned_data["start_date"]
    end_date = form.cleaned_data["end_date"]

    reservations = Reservation.objects.filter(
        created_at__range=(start_date, end_date)
    )

    # CSV setup
    opts = Reservation._meta
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="{opts.verbose_name_plural}.csv"'
    )

    writer = csv.writer(response)
    headers = [
        "Patient Name",
        "Doctor Name",
        "Approved",
        "Appointment Date",
        "Created At",
    ]
    writer.writerow(headers)

    for r in reservations.select_related("patient__user", "doctor__user"):
        writer.writerow(
            [
                r.patient.user.first_name,
                r.doctor.user.first_name,
                "Yes" if r.is_approved else "No",
                r.appointment,
                r.created_at,
            ]
        )

    return response

