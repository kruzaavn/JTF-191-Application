# chat/views.py
from django.shortcuts import render
from rest_framework import generics
from .serializers import DCSServerSerializer, DCSListServerSerializer
from .models import DCSServer


def index(request):
    return render(request, 'gci/index.html', {})


def room(request, room_name):
    return render(request, 'gci/room.html', {
        'room_name': room_name
    })


class ServerDetailView(generics.CreateAPIView):

    queryset = DCSServer.objects.all()
    serializer_class = DCSServerSerializer


class ServerListView(generics.ListAPIView):
    queryset = DCSServer.objects.all()
    serializer_class = DCSListServerSerializer
