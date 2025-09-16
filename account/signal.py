from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from profile_users.models import DoctorProfile , PatientProfile




@receiver(post_save,sender=User)
def linking_user_with_profile(sender,instance,created,**kwargs):
     if created:
          