from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated , AllowAny
from .models import Conversation , Message
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializer import MessageSerializer , ConversationSerializer


User = get_user_model()

class RealTimeChat(APIView):
     permission_classes = [IsAuthenticated]

     # start conversation
     def get(self,request,other_user_id):
          me = request.user
          other = get_object_or_404(User,id=other_user_id)

          if not other:
               return Response({'error':'user doesn\'t exist '},status=status.HTTP_400_BAD_REQUEST)
          
          if me.role == "patient" and other.role == "doctor":
               doctor_id , patient_id = other.id , me.id
          if me.role == "doctor" and other.role == "patient":
               doctor_id , patient_id = me.id , other.id

          conversation , _ = Conversation.objects.get_or_create(doctor=doctor_id,patient=patient_id)

          messages = conversation.messages.all().order_by('-created_at')

          conversation_data = ConversationSerializer(conversation).data
          messages_data = MessageSerializer(messages).data

          return Response({'messages':messages_data,'conversation':conversation_data},status=status.HTTP_200_OK)


