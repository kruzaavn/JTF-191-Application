from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import Aviator
from .serializers import AviatorSerializer
# Create your views here.


class AviatorListView(ListCreateAPIView):

    queryset = Aviator.objects.all()
    serializer_class = AviatorSerializer