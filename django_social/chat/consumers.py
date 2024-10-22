import json
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import Chat, Message
from account.models import User



class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def get_all_messages(self):
        username1, username2 = self.room_name.split('-')
        user1, user2 = User.objects.get(username=username1), User.objects.get(username=username2)
        chat = Chat.objects.filter(users=user1).filter(users=user2).first()
        messages = Message.objects.filter(chat=chat)
        dic = [ {
                    'message':message.content, 
                    'user':message.user.username, 
                    'timestamp': message.created.isoformat() 
                    } 
                for message in messages]
        return dic
    
    @database_sync_to_async
    def save_message(self, message):
        username1, username2 = self.room_name.split('-')
        user1, user2 = User.objects.get(username=username1), User.objects.get(username=username2)
        chat = Chat.objects.filter(users=user1).filter(users=user2).first()

        message = Message.objects.create(user=self.scope['user'], chat=chat, content=message)
        message.save()
        print('the message has been saved.')
        return message
    
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        messages_dict = await self.get_all_messages()
        await self.accept()
        await self.send(text_data=json.dumps({
            'messages': messages_dict
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = self.scope['user'].username
        messages_dict = await self.get_all_messages()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": username,  
                "messages": messages_dict
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        await self.save_message(message)
        await self.send(text_data=json.dumps({
            "message": message,
            "user": user,  
        }))




