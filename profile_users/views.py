from django.shortcuts import render , redirect , get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import DoctorProfile , PatientProfile , DoctorRating
from user_account.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import *
from django.urls import reverse_lazy
from datetime import date
from home.models import Reservation
from django.contrib import messages

@method_decorator(login_required(login_url='user_account:login'),name='dispatch')
class ProfilePatient(DetailView):
     model = PatientProfile
     template_name = 'profile/profile_patient.html'
     context_object_name = 'patient'

     def get_object(self):
          return self.request.user.patient
     
     @staticmethod
     def calculate_age(date_of_birth):
        if not date_of_birth:
            return "-"
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        return age
     
     def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         patient_profile = self.get_object()
         print(patient_profile)
         context['patient'] = patient_profile
         context['age'] = self.calculate_age(patient_profile.date_of_birthday)
         return context  

@method_decorator(login_required(login_url='user_account:login'), name='dispatch')
class BaseProfileUpdateView(UpdateView):
    user_form_class = None  
    template_name = None
    success_url = None      
    model_field = None      

    def get_object(self, queryset=None):
        return getattr(self.request.user, self.model_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["user_form"] = self.user_form_class(self.request.POST, instance=self.request.user)
        else:
            context["user_form"] = self.user_form_class(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context["user_form"]

        if user_form.is_valid() and form.is_valid():
            user_form.save()
            form.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(context)


class PatientProfileUpdateView(BaseProfileUpdateView):
    user_form_class = UserForm
    form_class = PatientProfileForm
    template_name = 'profile/edit_patient.html'
    model_field = 'patient'
    success_url = reverse_lazy('profile:profile_patient')


class ShowAppointment(ListView):
    model = Reservation
    template_name = 'home/reservation_list.html'

    def get_queryset(self):
        return Reservation.objects.filter(patient=self.request.user.patient)
    

def rate_doctor(request,doctor_id):
    doctor = get_object_or_404(DoctorProfile,id=doctor_id)
    patient = request.user

    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')
        

        DoctorRating.objects.update_or_create(
            doctor=doctor,
            patient=patient,
            defaults={"rating": rating, "comment": comment}
        )
        messages.success(request, "Your rating has been submitted!")
        return redirect("home:detials", doctor_id=doctor.id)