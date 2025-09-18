from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from profile_users.models import DoctorProfile , PatientProfile




@receiver(post_save,sender=User)
def linking_user_with_profile(sender,instance,created,**kwargs):
     if created:
          if instance.role == 'patient':
               PatientProfile.objects.create(user=instance)
          elif instance.role == 'doctor':
               DoctorProfile.objects.create(user=instance)