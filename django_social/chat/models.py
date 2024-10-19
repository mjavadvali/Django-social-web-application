from django.db import models
from account.models import User

class Chat(models.Model):
    users = models.ManyToManyField(User, related_name='chat_users')
    
    def chat_room_name(self, user1, user2):
        sorted_usernames = sorted([user1.username, user2.username])
        return f'{sorted_usernames[0]}-{sorted_usernames[1]}'
    
    def __str__(self):
        users = self.users.all()
        sorted_username = sorted([users[0].username, users[1].username])
        return f'{sorted_username[0]}-{sorted_username[1]}'


class Message(models.Model):
    user= models.ForeignKey(User, related_name='user_message', on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, related_name='chat_message', on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'message by {self.user.username} in {self.chat}'

     
