from django.contrib import admin
from .models import Reservation
from unfold.admin import ModelAdmin

@admin.register(Reservation)
class ReservationAdmin(ModelAdmin):
    fields = [field.name for field in Reservation._meta.get_fields()]
