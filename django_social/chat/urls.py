﻿from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('private_chat/<str:username>', views.private_chat, name='private_chat')
]