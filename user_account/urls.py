from django.urls import path , include
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import *
from .api_view import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r"api/register",,basename='api/register')






app_name = 'user_account'

urlpatterns = [
     path('',SignUp.as_view(),name='sign-up'),
     path('login/', CustomLoginView.as_view(), name='login'),
     path("logout/", LogoutView.as_view(next_page="user_account:login"), name="logout"),
     path('password_reset/',auth_views.PasswordResetView.as_view(success_url=reverse_lazy('user_account:password_reset_done')),name='password_reset'),
     path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
     path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('user_account:password_reset_complete')),name='password_reset_confirm'),
     path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
     path('verify-email/<token>/<uid>/',verify_email,name='verify_email'),
           # API
     path('api/register/',RegisterAPIView.as_view(),name='api_register'),
     path('api/login/', CustomLoginAPIView.as_view(), name='api_login'),
     
     
     path('',include(router.urls)),
]