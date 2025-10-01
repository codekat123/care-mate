from django.shortcuts import render , get_object_or_404
from .models import AIConversation, AIMessage
from .tasks import analyze_symptoms_task
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import ConversationSerializer, MessageSerializer


class AIChatAPIView(APIView):
    def get(self, request):
        conversation, _ = AIConversation.objects.get_or_create(user=request.user)


        messages = conversation.messages.order_by('-timestamp')[:20]


        conversation_data = ConversationSerializer(conversation).data
        messages_data = MessageSerializer(messages, many=True).data

        return Response(
            {"conversation": conversation_data, "messages": messages_data},
            status=status.HTTP_200_OK
        )



class SendMessageAPIView(APIView):

    def post(self, request):
        message = request.data.get("message")

        if not message:
            return Response(
                {"error": "Message cannot be empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get or create conversation for this user
        conversation, _ = AIConversation.objects.get_or_create(user=request.user)

        # Save user message
        user_msg = AIMessage.objects.create(
            conversation=conversation,
            message_type="user",
            content=message
        )

        # Get the last 10 messages before this one
        recent_messages = (
            conversation.messages.filter(id__lt=user_msg.id)
            .order_by('-timestamp')[:10]
        )

        recent_messages_list = [
            {"message_type": m.message_type, "content": m.content}
            for m in recent_messages
        ]

        # Send message to Celery task
        async_result = analyze_symptoms_task.apply_async(
            args=[message, recent_messages_list]
        )

        ai_response = async_result.get(timeout=20)

        # Save AI response
        ai_msg = AIMessage.objects.create(
            conversation=conversation,
            message_type="ai",
            content=ai_response,
        )

        # Serialize the AI message
        ai_msg_data = MessageSerializer(ai_msg).data

        return Response(
            {
                "user_message": message,
                "ai_response": ai_response,
                "timestamp": ai_msg.timestamp.isoformat(),
                "conversation": conversation.id,
                "ai_message": ai_msg_data,
            },
            status=status.HTTP_200_OK
        )