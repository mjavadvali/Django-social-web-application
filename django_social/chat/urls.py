from django.urls import path
from . import views

urlpatterns = [
    path('private_room/<str:username>', views.private_room, name='private_room')
]
