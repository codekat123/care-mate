from django.shortcuts import render , redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import DoctorProfile , PatientProfile
from user_account.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import *
from django.urls import reverse_lazy
from datetime import date
@method_decorator(login_required(login_url='user_account:login'),name='dispatch')
class ProfileDoctor(ListView):
     model = DoctorProfile
     template_name = 'profile/profile_doctor.html'
     context_object_name = 'doctor_profile'

     def get_object(self,queryset=None):
          return self.request.user.doctor


@method_decorator(login_required(login_url='user_account:login'),name='dispatch')
class ProfilePatient(ListView):
     model = PatientProfile
     template_name = 'profile/profile_patient.html'
     context_object_name = 'patient_profile'

     def get_object(self):
          return self.request.user.patient
     
     @staticmethod
     def calculate_age(date_of_birth):
        if not date_of_birth:
            return "-"
        today = date.today()
        return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

     def get_context_data(self,**kwargs):
         context = super().get_context_data(**kwargs)
         patient_profile = self.request.user.patient
         print(patient_profile)
         context['patient_profile'] = patient_profile
         context['age'] = self.calculate_age(patient_profile.date_of_birthday)  

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


class DoctorProfileUpdateView(BaseProfileUpdateView):
    user_form_class = UserForm
    form_class = DoctorProfileForm
    template_name = 'profile/edit_doctor.html'
    model_field = 'doctor'
    success_url = reverse_lazy('profile:profile_doctor')

class PatientProfileUpdateView(BaseProfileUpdateView):
    user_form_class = UserForm
    form_class = PatientProfileForm
    template_name = 'profile/edit_patient.html'
    model_field = 'patient'
    success_url = reverse_lazy('profile:profile_patient')