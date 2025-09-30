from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .models import User
from .serializer import SignUpSerializer , CustomLoginSerializer
from .tasks import send_validation_email
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from django.utils.encoding import force_str



class RegisterAPIView(CreateAPIView):
     queryset = User.objects.all()
     serializer_class = SignUpSerializer

     def perform_create(self,serializer):
        user = serializer.save(is_active=False) 
        protocol = "https" if self.request.is_secure() else "http"
        domain = self.request.get_host()
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)

        send_validation_email.delay(
            domain, protocol, uid, token, user.first_name, user.email , True
        )
        return user

     def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Check your email to activate your account"},
            status=status.HTTP_201_CREATED,
        )
     
class CustomLoginAPIView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer


def verify_email(request, token, uid):
    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response(
            {
                "success": True,
                "message": "Your account has been activated successfully 🎉",
                "next_step": "You can now log in and access your dashboard."
            },
            status=status.HTTP_200_OK)
    return Response(
    {
        "success": False,
        "message": "something went wrong",
        "next_step": "try again"
    },
    status=status.HTTP_400_BAD_REQUEST
)

