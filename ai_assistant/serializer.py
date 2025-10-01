from rest_framework import serailizer
from .models import AIConversation , AIMessage

class ConversationSerializer(serailizer.ModelSerializer):
     class Meta:
          model = AIConversation
          fields = '__all__'

class MessageSerializer(serailizer.ModelSerializer):
     class Meta:
          model = AIMessage
          fields = '__all__'
