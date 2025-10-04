from django.contrib import admin
from .models import AIConversation , AIMessage
from unfold.admin import ModelAdmin

@admin.register(AIConversation)
class AIConversationAdmin(ModelAdmin):
    fields = [field.name for field in AIConversation._meta.get_fields()]

@admin.register(AIMessage)
class AIMessageAdmin(ModelAdmin):
    fields = [field.name for field in AIMessage._meta.get_fields()]