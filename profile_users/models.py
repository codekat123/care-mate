from django.db import models
from account.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

class PatientProfile(models.Model):
     user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user')
     date_of_birthday = models.DateField(null=True,blank=True)
     gender = models.CharField(max_length=40,choices=[("M", "Male"), ("F", "Female")],null=True,blank=True)
     address = models.CharField(max_length=200,null=True,blank=True)
     phone_number = models.CharField(max_length=200,null=True,blank=True)
     profile_image = models.ImageField(upload_to="patients/", blank=True, null=True)

     def __str__(self):
        return f"Patient: {self.user.username}"



class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    hospital = models.CharField(max_length=150, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="doctors/", blank=True, null=True)
    rate = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(10)], blank=True, null=True)
    
    def __str__(self):
        return f"Dr. : {self.user.username}"