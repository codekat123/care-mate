from django.shortcuts import render ,redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate , login 
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from .models import User
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from .tasks import send_reset_email , send_validation_email
from django.conf import settings
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str



class SignUp(CreateView):
     model = User
     form_class = SignUpForm
     template_name = 'user_account/sign_up.html'

     def form_valid(self, form):
         user = form.save(commit=False)
         user.is_active = False
         user.save() 
         protocal = 'https' if self.request.is_secure() else 'http'
         domain = self.request.get_host()
         uid = urlsafe_base64_encode(force_bytes(user.id))
         token = default_token_generator.make_token(user)
         send_validation_email.delay(domain,protocal,uid,token,user.first_name,user.email)
         
         return super().form_valid(form)



     
     def get_success_url(self):
          messages.success(self.request,'chcek your email to active your account')
          return reverse_lazy('user_account:login')

     def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
          if self.request.user.role == 'doctor':
            return redirect('dashboard:dashboard')
          return redirect('home:doctor')
        return super().get(*args, **kwargs)

class CustomLoginView(LoginView):
    template_name = 'user_account/login.html'
    redirect_authenticated_user = True
    authentication_form = EmailAuthenticationForm

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

    def form_valid(self, form):
        """ Extra validation after successful authentication """
        user = form.get_user()


        if not user.is_active:
            messages.error(self.request, "Your account is not active. Please verify your email.")
            return redirect("user_account:login")

        if user.role == "doctor" and user.doctor.is_completed:
            messages.info(self.request, "Please complete your profile before continuing.")
        
        if user.role == "patient" and user.patient.is_completed:
            messages.info(self.request, "Please complete your profile before continuing.")


        return super().form_valid(form)



class AsyncPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,context, from_email, to_email, html_email_template_name=None):
        subject = self.render_mail_subject(subject_template_name, context)
        body = self.render_mail_body(email_template_name, context)
        html_body = None
        if html_email_template_name:
            html_body = self.render_mail_body(html_email_template_name, context)

        
        send_reset_email.delay(subject, body, from_email or settings.DEFAULT_FROM_EMAIL, [to_email], html_body)


def verify_email(request, token, uid):
    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated!')
        return redirect('user_account:login')

    messages.error(request, 'Something went wrong.')
    return redirect('user_account:sign-up')

