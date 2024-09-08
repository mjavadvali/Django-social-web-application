from django.db import models
from account.models import User

class Chat(models.Model):
    users = models.ManyToManyField(User, related_name='chat_users')

    def chat_room_name(self, user1, user2):
        return f'{user1.id}{user2.id}'
    
    def __str__(self):
        users = self.users.all()

        return f'{users[0].username}-{users[1].username}'


class Message(models.Model):
    user= models.ForeignKey(User, related_name='user_message', on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, related_name='chat_message', on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'message by {self.user.username} in {self.chat}'

     
