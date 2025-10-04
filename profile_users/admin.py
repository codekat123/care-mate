from django.contrib import admin
from .models import PatientProfile , DoctorProfile , DoctorRating
from unfold.admin import ModelAdmin

@admin.register(PatientProfile)
class PatientProfileAdmin(ModelAdmin):
    fields = [field.name for field in PatientProfile._meta.get_fields()]

@admin.register(DoctorProfile)
class DoctorProfileAdmin(ModelAdmin):
    fields = [field.name for field in DoctorProfile._meta.get_fields()]

@admin.register(DoctorRating)
class DoctorRatingAdmin(ModelAdmin):
    fields = [field.name for field in DoctorRating._meta.get_fields()]