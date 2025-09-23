from django.urls import path
from .views import *

app_name = 'home'

urlpatterns =[
          path('',HomeView.as_view(),name='doctor'),
          path('doctor_detail/<int:doctor_id>/',DoctorDetials.as_view(),name='detials'),
          path("search/", SearchView.as_view(), name="search"),

          ]