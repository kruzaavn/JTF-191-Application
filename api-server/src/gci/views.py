# chat/views.py
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, authentication

from .serializers import DCSServerSerializer, DCSListServerSerializer
from .models import DCSServer


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
