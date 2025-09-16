from django.urls import path
from .views import *
app_name = 'account'

urlpatterns = [
     path('',SignUp.as_view(),name='sign-up'),
      path('login/', CustomLoginView.as_view(), name='login'),
]