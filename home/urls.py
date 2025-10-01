from django.urls import path
from .views import *
from .api_view import *
app_name = 'home'

urlpatterns =[
          path('',HomeView.as_view(),name='doctor'),
          path('doctor_detail/<int:doctor_id>/',DoctorDetials.as_view(),name='detials'),
          path("search/", SearchView.as_view(), name="search"),

          #API
          path('api/home/doctor/',ListHome.as_view(),name='api-home'),
          path('api/detail/doctor/<int:pk>/',DetailHome.as_view(),name='api-detail'),

          ]