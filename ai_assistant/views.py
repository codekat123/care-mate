# app_name/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views import View
import json

from .models import AIConversation, AIMessage
from .service import GeminiMedicalAssistant


@method_decorator(login_required, name="dispatch")
class AIChatView(View):
    template_name = "ai_assistant/chat.html"

    def get(self, request):
        
        conversation, created = AIConversation.objects.get_or_create(user=request.user)

        
        messages = conversation.messages.all().order_by("-timestamp")[:20]
        messages = reversed(messages)  

        context = {
            "conversation": conversation,
            "messages": messages,
        }
        return render(request, self.template_name, context)


@csrf_exempt
@require_POST
@login_required
def send_message(request):
    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()

        if not user_message:
            return JsonResponse({"error": "Message cannot be empty"}, status=400)

        
        conversation, created = AIConversation.objects.get_or_create(user=request.user)

        
        user_msg = AIMessage.objects.create(
            conversation=conversation,
            message_type="user",
            content=user_message,
        )

        
        recent_messages = conversation.messages.filter(
            id__lt=user_msg.id
        ).order_by("-timestamp")[:10]

        
        ai_service = GeminiMedicalAssistant()
        ai_response = ai_service.analyze_symptoms(user_message,recent_messages)

       
        ai_msg = AIMessage.objects.create(
            conversation=conversation,
            message_type="ai",
            content=ai_response,
        )

        return JsonResponse(
            {
                "user_message": user_message,
                "ai_response": ai_response,
                "timestamp": ai_msg.timestamp.isoformat(),
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
