import google.generativeai as genai
from django.conf import settings
from celery import shared_task


SYSTEM_PROMPT = (
    """
    You are a medical AI assistant for a doctor appointment booking system.
    Your role is to:
    1. Listen to user symptoms
    2. Provide general health guidance (not medical diagnosis)
    3. Recommend whether they should book an appointment or try home remedies
    4. Always emphasize that you are not a doctor and serious symptoms need professional care

    Guidelines:
    - For mild symptoms (headache, minor stomach ache): suggest home remedies and monitoring
    - For serious symptoms (chest pain, difficulty breathing, severe pain): strongly recommend immediate doctor consultation
    - Always end with: "If symptoms worsen or persist, please consult a healthcare professional"
    - Be empathetic and clear in your responses
    - Keep responses concise but helpful
    """
)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def analyze_symptoms_task(self, user_message, conversation_history=None):
    try:
        # Configure Gemini in the worker process
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("models/gemini-1.5-flash")

        messages = [{"role": "model", "parts": [SYSTEM_PROMPT]}]

        if conversation_history:
            for msg in conversation_history:
                role = "user" if msg.get("message_type") == "user" else "model"
                messages.append({"role": role, "parts": [msg.get("content", "")]})

        messages.append({"role": "user", "parts": [user_message]})
        response = model.generate_content(messages)

        return response.candidates[0].content.parts[0].text.strip()

    except Exception as exc:
        raise exc
