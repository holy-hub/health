from django.shortcuts import render
from .authentification.models import *

# Create your views here.
def chat_room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'title': room_name,
    })
    
def chat_room(request, room_name):
    users = Utilisateur.objects.exclude(user=request.user)
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'users': users
    })