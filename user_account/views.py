from django.shortcuts import render ,redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate , login 
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from .models import User
from .forms import SignUpForm
from django.contrib import messages


class SignUp(CreateView):
     model = User
     form_class = SignUpForm
     template_name = 'user_account/sign_up.html'

     def form_valid(self, form):
         user = form.save()
         raw_password = form.cleaned_data.get("password1")
         authenticated_user = authenticate(
             self.request,
             username=user.username,
             password=raw_password
         )
         if authenticated_user is not None:
             login(self.request, authenticated_user)
             if authenticated_user.role == 'doctor':
                 return redirect('dashboard:dashboard')
             return redirect('home:doctor')
     
         return super().form_invalid(form)


     
     def get_success_url(self):
          messages.warning(self.request,'please complete your info from profile section')
          if self.request.user.role == 'doctor':
               return reverse_lazy('dashboard:dashboard')
          return reverse_lazy('home:doctor')

     def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
          if self.request.user.role == 'doctor':
            return redirect('dashboard:dashboard')
          return redirect('home:doctor')
        return super().get(*args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'user_account/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
          
          if self.request.user.role == 'doctor':
               return reverse_lazy('dashboard:dashboard')
          return reverse_lazy('home:doctor')

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
          if self.request.user.role == 'doctor':
            return redirect('dashboard:dashboard')
          return redirect('home:doctor')
        return super().get(*args, **kwargs)






