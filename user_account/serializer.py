from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class SignUpSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ['first_name','last_name','email','password']
          extra_kwargs = {"password":{"write_only":True}}

     def create(self,validated_data):
          user = User.objects.create_user(**validated_data)
          return user
     

class CustomLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  # authenticates user and creates tokens
        user = getattr(self, "user", None)

        if user is None:
            raise serializers.ValidationError({"error": "Authentication failed."})


        if not user.is_active:
            raise serializers.ValidationError(
                {"error": "Your account is not active. Please verify your email."}
            )

    
        extra_info = []
        if getattr(user, "role", None) == "doctor":
            doctor = getattr(user, "doctor", None)
            if doctor and not getattr(doctor, "is_completed", False):
                extra_info.append("Please complete your doctor profile before continuing.")
        elif getattr(user, "role", None) == "patient":
            patient = getattr(user, "patient", None)
            if patient and not getattr(patient, "is_completed", False):
                extra_info.append("Please complete your patient profile before continuing.")

        if extra_info:
            data["info"] = " ".join(extra_info)

        # Optionally add non-sensitive user info to response
        data["user"] = {
            "id": user.id,
            "email": user.email,
            "role": getattr(user, "role", None),
        }

        return data

    