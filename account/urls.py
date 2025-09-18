from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *
app_name = 'account'

urlpatterns = [
     path('',SignUp.as_view(),name='sign-up'),
      path('login/', CustomLoginView.as_view(), name='login'),
      path("logout/", LogoutView.as_view(next_page="account:login"), name="logout"),
]