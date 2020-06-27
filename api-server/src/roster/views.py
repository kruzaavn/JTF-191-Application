from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Aviator, Squadron, HQ
from .serializers import AviatorSerializer, SquadronSerializer, HQSerializer
# Create your views here.


class AviatorListView(ListCreateAPIView):

    queryset = Aviator.objects.all().order_by('-rank_code', '-position_code')
    serializer_class = AviatorSerializer


class AviatorDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Aviator.objects.all()
    serializer_class = AviatorSerializer


class SquadronListView(ListCreateAPIView):
    queryset = Squadron.objects.all()
    serializer_class = SquadronSerializer


class HQListView(ListCreateAPIView):
    queryset = HQ.objects.all()
    serializer_class = HQSerializer
