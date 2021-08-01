from rest_framework import serializers
from .models import *


class DCSServerSerializer(serializers.ModelSerializer):

    class Meta:
        model = DCSServer
        fields = '__all__'
