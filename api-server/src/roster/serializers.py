from rest_framework import serializers
from .models import *


class HQSerializer(serializers.ModelSerializer):

    class Meta:
        model = HQ
        fields = '__all__'


class SquadronSerializer(serializers.ModelSerializer):

    class Meta:
        model = Squadron
        fields = '__all__'
        depth = 1


class OperationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Operation
        fields = '__all__'


class AviatorSerializer(serializers.ModelSerializer):

    rank = serializers.ReadOnlyField()
    position = serializers.ReadOnlyField()

    class Meta:
        model = Aviator
        exclude = ['first_name', 'last_name', 'user', 'email']
        depth = 2


class ProspectiveAviatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProspectiveAviator
        fields = '__all__'


class DCSModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = DCSModules
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
        depth = 1


class QualificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Qualification
        fields = '__all__'


class QualificationModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = QualificationModule
        fields = '__all__'


class QualificationCheckoffSerializer(serializers.ModelSerializer):

    current = serializers.ReadOnlyField()

    class Meta:
        model = QualificationCheckoff
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password', 'user_permissions', 'first_name', 'last_name', 'email']
