from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Conversation, Message
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
User = get_user_model()

# @login_required
# def conversations_list(request):
#     user = request.user
#     conversations = Conversation.objects.filter(
#         Q(doctor_id=user.id) | Q(patient_id=user.id)
#     ).select_related('doctor', 'patient').order_by('-created_at')

#     context = {
#         'conversations': conversations,
#     }
#     return render(request, 'chat/conversations.html', context)

@login_required
def start_conversation(request, other_user_id):
    me = request.user
    other = get_object_or_404(User, id=other_user_id)

    if me.role == 'patient' and other.role == 'patient':
        return redirect('/')
    if me.role == 'doctor' and other.role == 'doctor':
        return redirect('/')

    if me.role == 'doctor' and other.role == 'patient':
        doctor_id, patient_id = me.id, other.id
    elif me.role == 'patient' and other.role == 'doctor':
        doctor_id, patient_id = other.id, me.id
    else:
        return redirect('/')

    conv, _ = Conversation.objects.get_or_create(doctor_id=doctor_id, patient_id=patient_id)
    return redirect('chat:room', conversation_id=conv.id)

@login_required
def room(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)


    if request.user.id not in (conversation.doctor.id, conversation.patient.id):
        return redirect('/')

    messages = conversation.messages.select_related('sender').all()
    return render(request, 'chat/room.html', {
        'conversation': conversation,
        'messages': messages,
    })

@method_decorator(login_required(login_url='user_account:login'),name='dispatch')
class ConversationListDoctor(ListView):
    model = Conversation
    template_name = 'chat/doctor_conversation.html'
    context_object_name = "conversations"


    def get_queryset(self):
        if self.request.user.role == "doctor":
            return Conversation.objects.filter(doctor=self.request.user).select_related('doctor', 'patient').order_by('-created_at')
        return Conversation.objects.filter(patient=self.request.user).select_related('doctor', 'patient').order_by('-created_at')

