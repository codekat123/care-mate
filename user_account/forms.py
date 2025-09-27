from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import User
from django import forms


class SignUpForm(UserCreationForm):
     class Meta:
          model = User
          fields = ['first_name','password1','password2','role','email']



class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autofocus': True})
    )

    def clean(self):
        email = self.cleaned_data.get("username")  # still called "username" internally
        password = self.cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid email or password.")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
