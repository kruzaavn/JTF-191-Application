from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Aviator, Squadron
from .serializers import AviatorSerializer, SquadronSerializer
# Create your views here.


class AviatorListView(ListCreateAPIView):

    queryset = Aviator.objects.all()
    serializer_class = AviatorSerializer


class AviatorDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Aviator.objects.all()
    serializer_class = AviatorSerializer


class SquadronListView(ListCreateAPIView):
    queryset = Squadron.objects.all()
    serializer_class = SquadronSerializer