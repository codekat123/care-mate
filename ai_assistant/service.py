import google.generativeai as genai
from django.conf import settings


class GeminiMedicalAssistant:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("models/gemini-1.5-flash")




        self.system_prompt = """
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

    def analyze_symptoms(self, user_message, conversation_history=None):
        try:
            messages = [{"role": "model", "parts": [self.system_prompt]}]

            if conversation_history:
                for msg in conversation_history:
                    role = "user" if msg.message_type == "user" else "model"
                    messages.append({"role": role, "parts": [msg.content]})

            messages.append({"role": "user", "parts": [user_message]})
            response = self.model.generate_content(messages)

            print("DEBUG - Gemini raw response:", response)
            return response.candidates[0].content.parts[0].text.strip()

        except Exception as e:
            import traceback
            print("DEBUG - Gemini Exception:", str(e))
            traceback.print_exc()
            return (
                "I'm sorry, I'm having trouble processing your request right now.\n"
                "Please try again."
            )

