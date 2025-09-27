from django.db import models
from user_account.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
from django.conf import settings
class PatientProfile(models.Model):
     user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='patient')
     date_of_birthday = models.DateField(null=True,blank=True)
     gender = models.CharField(max_length=40,choices=[("M", "Male"), ("F", "Female")],null=True,blank=True)
     address = models.CharField(max_length=200,null=True,blank=True)
     phone_number = models.CharField(max_length=200,null=True,blank=True)
     profile_image = models.ImageField(default="patients/patient.jpeg",upload_to="patients/", blank=True, null=True)

     def __str__(self):
        return f"Patient: {self.user.first_name}"
     
     @property
     def is_completed(self):
        return all([
            self.address,
            self.gender,
            self.date_of_birthday,
            self.phone_number,
            self.profile_image
        ])


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
        return f"Dr. : {self.user.first_name}"
    
    @property
    def is_completed(self):
        return all([
            self.major,
            self.major_description,
            self.consultation_fee,
            self.work_start_time,
            self.work_end_time,
            self.location_medical_office,
            self.phone_number,
            self.bio,
            self.profile_image
        ])
    @property
    def average_rating(self):
        ratings = self.ratings.all()  
        if ratings.exists():
            return round(sum(r.rating for r in ratings) / ratings.count(), 2)
        return 0  
    





class DoctorRating(models.Model):
    doctor = models.ForeignKey("DoctorProfile", on_delete=models.CASCADE, related_name="ratings")
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="given_ratings")
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("doctor", "patient") 

    def __str__(self):
        return f"{self.doctor.user.first_name} - {self.rating}⭐"
