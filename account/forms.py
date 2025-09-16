from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms


class SignUp(UserCreationForm):
     class Meta:
          model = User
          fields = ['username','first_name','password1','password2','role']
