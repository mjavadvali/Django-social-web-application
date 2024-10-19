from django.shortcuts import render, HttpResponse, get_object_or_404
from account.models import User
from .models import Chat
from urllib.parse import quote


def index(request):
    return render(request, "index.html")

def room(request, username):
    return render(request, "new_room.html", {"room_name": 'room'})


def private_chat(request, username):
    user1 = request.user
    user2 = get_object_or_404(User, username= username)

    if not Chat.objects.filter(users=user1).filter(users=user2).first():
        chat = Chat.objects.create()
        chat.users.set([user1, user2])
    else:
        chat = Chat.objects.filter(users=user1).filter(users=user2).first()

    room_name = chat.chat_room_name


    return render(request, "room.html", {"room_name": room_name})


def private_room(request, username):
    user1 = request.user
    user2 = get_object_or_404(User, username=username)
    chat = Chat.objects.filter(users=user1).filter(users=user2).first()

    if not chat:
        chat = Chat.objects.create()
        
        chat.users.set([user1, user2])

        chat.save()

    room_name = chat.chat_room_name(user1=user1, user2=user2)
    print('room_name:', room_name.split('-'))

    return render(request, 'private_room.html', {'room_name': room_name, 'user': user2})   