from rest_framework import serializers
from .models import *


class HQSerializer(serializers.ModelSerializer):

    class Meta:
        model = HQ
        fields = ['name', 'service']


class AirFrameSerializer(serializers.ModelSerializer):

    class Meta:
        model = AirFrame
        fields = '__all__'


class SquadronSerializer(serializers.ModelSerializer):

    class Meta:
        model = Squadron
        fields = '__all__'


class OperationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Operation
        fields = '__all__'


class AviatorSerializer(serializers.ModelSerializer):

    rank = serializers.ReadOnlyField()
    squadron = SquadronSerializer()
    operations = OperationSerializer()

    class Meta:
        model = Aviator
        fields = '__all__'
        depth = 2
