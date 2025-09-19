from django import forms
from .models import DoctorProfile , PatientProfile
from user_account.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ["profile_image", "bio","major","major_description","consultation_fee","work_start_time","work_end_time","phone_number",]
        widgets = {
                    "work_start_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
                    "work_end_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),}

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ["profile_image", "gender","date_of_birthday","address","phone_number"]