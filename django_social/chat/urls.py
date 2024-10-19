from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('<str:room_name>/', views.room, name='new_room'),
    path('pv/<str:username>', views.room, name='pv'),

    path('private_chat/<str:username>', views.private_chat, name='private_chat'),
    path('private_room/<str:username>', views.private_room, name='private_room')
]
