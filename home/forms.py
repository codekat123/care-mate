from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
     class Meta:
          model = Reservation
          fields = ['name','phone_number']

          widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
        }