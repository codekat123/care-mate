from django.db import models
from user_account.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

class PatientProfile(models.Model):
     user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='patient')
     date_of_birthday = models.DateField(null=True,blank=True)
     gender = models.CharField(max_length=40,choices=[("M", "Male"), ("F", "Female")],null=True,blank=True)
     address = models.CharField(max_length=200,null=True,blank=True)
     phone_number = models.CharField(max_length=200,null=True,blank=True)
     profile_image = models.ImageField(default="patients/patient.jpeg",upload_to="patients/", blank=True, null=True)

     def __str__(self):
        return f"Patient: {self.user.username}"


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor")
    major = models.CharField(max_length=200,blank=True, null=True)
    major_description = models.CharField(max_length=500,blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=7, decimal_places=2,blank=True,null=True)
    work_start_time = models.TimeField(null=True, blank=True)
    work_end_time = models.TimeField(null=True, blank=True)
    location_medical_office = models.TextField(max_length=400,null=True,blank=True)
    phone_number = models.CharField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(default="doctors/doctor.jpeg",upload_to="doctors/", blank=True, null=True)
    
    def __str__(self):
        return f"Dr. : {self.user.username}"