from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Conversation, Message

User = get_user_model()

@login_required
def conversations_list(request):
    user = request.user
    conversations = Conversation.objects.filter(
        Q(doctor_id=user.id) | Q(patient_id=user.id)
    ).select_related('doctor', 'patient').order_by('-created_at')

    context = {
        'conversations': conversations,
    }
    return render(request, 'chat/conversations.html', context)

@login_required
def start_conversation(request, other_user_id):
    me = request.user
    other = get_object_or_404(User, id=other_user_id)

    # Enforce: only doctor-patient pairs allowed; patients cannot start with patients; doctors cannot start with doctors
    if me.role == 'patient' and other.role == 'patient':
        return redirect('chat:conversations')
    if me.role == 'doctor' and other.role == 'doctor':
        return redirect('chat:conversations')

    if me.role == 'doctor' and other.role == 'patient':
        doctor_id, patient_id = me.id, other.id
    elif me.role == 'patient' and other.role == 'doctor':
        doctor_id, patient_id = other.id, me.id
    else:
        # If roles are missing/invalid, deny
        return redirect('chat:conversations')

    conv, _ = Conversation.objects.get_or_create(doctor_id=doctor_id, patient_id=patient_id)
    return redirect('chat:room', conversation_id=conv.id)

@login_required
def room(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Enforce membership and correct roles
    if request.user.id not in (conversation.doctor_id, conversation.patient_id):
        return redirect('chat:conversations')

    messages = conversation.messages.select_related('sender').all()
    return render(request, 'chat/room.html', {
        'conversation': conversation,
        'messages': messages,
    })
