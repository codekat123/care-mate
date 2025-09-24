import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Conversation, Message


User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get('user')
        if user is None or not user.is_authenticated:
            await self.close()
            return

        conversation_id = self.scope['url_route']['kwargs'].get('conversation_id')

        conversation = await self.get_conversation(conversation_id)
        if conversation is None:
            await self.close()
            return

        is_member = await self.is_user_in_conversation(conversation, user)
        if not is_member:
            await self.close()
            return

        self.conversation_id = conversation_id
        self.room_group_name = f"conversation_{conversation_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        user = self.scope.get('user')
        if text_data is None or user is None or not user.is_authenticated:
            return

        try:
            payload = json.loads(text_data)
        except Exception:
            return

        content = (payload.get('content') or '').strip()
        if not content:
            return

        message = await self.create_message(self.conversation_id, user.id, content)

        event = {
            'type': 'chat.message',
            'message': {
                'id': message['id'],
                'sender_id': message['sender_id'],
                'content': message['content'],
                'created_at': message['created_at'],
            }
        }
        await self.channel_layer.group_send(self.room_group_name, event)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    # DB helpers
    @database_sync_to_async
    def get_conversation(self, conversation_id):
        try:
            return Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return None

    @database_sync_to_async
    def is_user_in_conversation(self, conversation, user):
        return conversation.doctor.id == user.id or conversation.patient.id == user.id

    @database_sync_to_async
    def create_message(self, conversation_id, user_id, content):
        message = Message.objects.create(
            conversation_id=conversation_id,
            sender_id=user_id,
            content=content,
        )
        return {
            'id': message.id,
            'sender_id': message.sender_id,
            'content': message.content,
            'created_at': message.created_at.isoformat(),
        }


