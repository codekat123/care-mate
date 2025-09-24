from django.urls import path
from . import views

app_name = 'chat'


urlpatterns =[
    # path('', views.conversations_list, name='conversations'),
    path('start/<int:other_user_id>/', views.start_conversation, name='start'),
    path('room/<int:conversation_id>/', views.room, name='room'),
    path('doctor-conversation/',views.ConversationListDoctor.as_view(),name='doctor_conversations')
]