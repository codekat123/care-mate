from django.contrib import admin
from .models import User
from unfold.admin import ModelAdmin

@admin.register(User)
class UserAdmin(ModelAdmin):
    fields = [field.name for field in User._meta.get_fields()]

