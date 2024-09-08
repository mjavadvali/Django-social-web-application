from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Chat 


User = get_user_model()

class ChatModelTest(TestCase):

    def setUp(self):
        # Create two test users
        self.user1 = User.objects.create_user(username='user1', password='Mj@972013037', email="alqi@gmail.com")
        self.user2 = User.objects.create_user(username='user2', password='pMj@972013037', email="ali@gmail.com")

        self.chat = Chat.objects.create()
        self.chat.users.set([self.user1, self.user2])

    def test_chat_room_name(self):
        expected_room_name = f'{self.user1.id}{self.user2.id}'
        self.assertEqual(self.chat.chat_room_name(self.user1, self.user2), expected_room_name)

        # Ensure that the order of users does not affect the room name
        expected_room_name_reverse = f'{self.user2.id}{self.user1.id}'
        self.assertEqual(self.chat.chat_room_name(self.user2, self.user1), expected_room_name_reverse)