from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Aviator
from .serializers import AviatorSerializer
# Create your views here.


class AviatorListView(ListCreateAPIView):

    queryset = Aviator.objects.all()
    serializer_class = AviatorSerializer


class AviatorDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Aviator.objects.all()
    serializer_class = AviatorSerializer
