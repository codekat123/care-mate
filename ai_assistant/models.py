from django.db import models
from user_account.models import User

class AIConversation(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='ai_conversation')
     created_at = models.DateTimeField(auto_now_add=True)
     update_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return f"AI Chat {self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
     

class AIMessage(models.Model):
     MESSAGE_TYPE = [
          ('user','user message'),
          ('AI','AI response')
     ]
     conversation = models.ForeignKey(AIConversation,on_delete=models.CASCADE,related_name='messages')
     message_type = models.CharField(max_length=10,choices=MESSAGE_TYPE)
     content = models.TextField()
     timestamp = models.DateTimeField(auto_now_add=True)

     class Meta:
          ordering = ['timestamp']