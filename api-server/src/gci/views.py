# chat/views.py
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, authentication

from .serializers import DCSServerSerializer, DCSListServerSerializer
from .models import DCSServer


def index(request):
    return render(request, 'gci/index.html', {})


def room(request, room_name):
    return render(request, 'gci/room.html', {
        'room_name': room_name
    })


class ServerDetailView(RetrieveUpdateDestroyAPIView):

    queryset = DCSServer.objects.all()
    serializer_class = DCSServerSerializer
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ServerListView(ListCreateAPIView):
    queryset = DCSServer.objects.all()
    serializer_class = DCSServerSerializer
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
