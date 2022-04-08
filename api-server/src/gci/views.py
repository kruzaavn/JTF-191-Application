# chat/views.py
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, authentication
from datetime import datetime, timedelta
from .serializers import DCSServerSerializer
from .models import DCSServer


class ServerDetailView(RetrieveUpdateDestroyAPIView):

    queryset = DCSServer.objects.all()
    serializer_class = DCSServerSerializer
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ServerListView(ListCreateAPIView):
    serializer_class = DCSServerSerializer
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):

        now = datetime.now()
        offset = timedelta(hours=5)

        return DCSServer.objects.filter(connection_time__range=[now - offset, now])