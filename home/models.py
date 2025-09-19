from django.db import models
from profile_users.models import PatientProfile , DoctorProfile


class Reservation(models.Model):
     patient = models.ForeignKey(PatientProfile,on_delete=models.CASCADE)
     doctor = models.ForeignKey(DoctorProfile,on_delete=models.CASCADE)
     is_approved = models.BooleanField(default=False)
     appointment = models.DateTimeField(null=True,blank=True)
     name = models.CharField(max_length=100,)
     phone_number = models.CharField(max_length=60)

     def __str__(self):
          return self.name