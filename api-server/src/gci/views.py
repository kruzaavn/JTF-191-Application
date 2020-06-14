# chat/views.py
from django.shortcuts import render


def index(request):
    return render(request, 'gci/index.html', {})


def room(request, room_name):
    return render(request, 'gci/room.html', {
        'room_name': room_name
    })