from django.contrib import admin
from .models import Conversation , Message
from unfold.admin import ModelAdmin


@admin.register(Conversation)
class ConversationAdmin(ModelAdmin):
    fields = [field.name for field in Conversation._meta.get_fields()]

@admin.register(Message)
class MessageAdmin(ModelAdmin):
    fields = [field.name for field in Message._meta.get_fields()]
