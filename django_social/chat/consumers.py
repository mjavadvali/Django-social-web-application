﻿import json
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import Chat, Message
from account.models import User
import uuid


class TempConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        messages_dict = await self.get_all_messages()
        await self.send(text_data=json.dumps({
            'messages': messages_dict
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
    
        await self.save_message(message)
       
        await self.channel_layer.group_send(
            self.room_group_name, 
            {
                "type": "chat_message",
                "message": message,
                "user" : username,
            }
        )
        await self.save_message(message)
            
    
    @database_sync_to_async
    def save_message(self, message):
        id_temp_1, id_temp_2 = self.room_name[:36], self.room_name[36:]
        id_1, id_2 = uuid.UUID(id_temp_1), uuid.UUID(id_temp_2)        
        user1, user2 = User.objects.get(pk=id_1), User.objects.get(pk=id_2)

        chat = Chat.objects.filter(users=user1).filter(users=user2).first()

        sender = User.objects.get(username=self.scope['user'])


        message = Message.objects.create(user=sender, chat=chat, content=message)
        message.save()
        print('the message has been saved.')
        return message
    
    @database_sync_to_async
    def get_all_messages(self):
        messages = Message.objects.all()
        dic = {m.content: m.user.username for m in messages}
        return dic
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user']
        }))