from django.shortcuts import render ,redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from .models import User
from .forms import SignUp

class SignUp(CreateView):
     model = User
     form_class = SignUp
     template_name = 'account/sign_up.html'
     success_url = reverse_lazy('#')
     def form_valid(self,form):
          user=form.save()
          login(self.request,user)
          return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = False

    def get_success_url(self):
         return self.request.path

def log_out(request):
     logout(request)
     return redirect('account:login')