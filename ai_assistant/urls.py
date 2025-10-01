# ai_assistant/urls.py
from django.urls import path
from . import views
from .api_view import *
app_name = 'ai_assistant'

urlpatterns = [
    path('chat/', views.AIChatView.as_view(), name='chat'),
    path('chat/send/', views.send_message, name='send_message'),
    path('chat/delete/<int:pk>/',views.DeleteAIConversation.as_view(),name='delete'),
    # API
    path('api/chat/',AIChatAPIView.as_view(),name='api_chat'),
    path('api/chat/send/',SendMessageAPIView.as_view(),name='api_send')
]
