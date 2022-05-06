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


class AwardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Award
        fields = '__all__'


class CitationSerializer(serializers.ModelSerializer):
    award = AwardSerializer(read_only=True)
    
    class Meta:
        model = Citation
        fields = '__all__'


class AviatorSerializer(serializers.ModelSerializer):

    rank = serializers.ReadOnlyField()
    position = serializers.ReadOnlyField()
    citations = serializers.SerializerMethodField()

    class Meta:
        model = Aviator
        exclude = ['user', 'email']
        depth = 2

    def get_citations(self, instance):
        citations = instance.citations.all().order_by('award__priority')
        return CitationSerializer(citations, many=True, read_only=True).data


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
        exclude = ['aviator']
        depth = 1

class EventCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


class DocumentationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Documentation
        fields = '__all__'


class DocumentationModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentationModule
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password', 'user_permissions', 'first_name', 'last_name', 'email']


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


class UserImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserImage
        fields = '__all__'



class MunitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Munition
        fields = '__all__'


class StoresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stores
        fields = '__all__'


class LiverySerializer(serializers.ModelSerializer):

    class Meta:
        model = Livery
        fields = '__all__'


class LiverySkinSerializer(serializers.ModelSerializer):

    class Meta:
        model = LiverySkin
        fields = '__all__'


class LiveryLuaSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = LiveryLuaSection
        fields = '__all__'


class TargetSerializer(serializers.ModelSerializer):

    type = serializers.ReadOnlyField()

    class Meta:
        model = Target
        fields = '__all__'


class FlightLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlightLog
        fields = '__all__'


class FlightLogAggregateSerializer(serializers.Serializer):

    total_flight_time = serializers.DurationField()
    platform_id = serializers.IntegerField()
    platform = serializers.CharField()

class FlightLogTimeSeriesSerializer(serializers.Serializer):

    total_flight_time = serializers.DurationField()
    date = serializers.DateField()


class CombatLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = CombatLog
        fields = '__all__'


class CombatLogAggregateSerializer(serializers.Serializer):

    kills = serializers.IntegerField()
    target_category = serializers.IntegerField()
    type = serializers.SerializerMethodField()

    def get_type(self, obj):

        if obj.target_category in [0, 1]:

            return 'air'

        elif obj.target_category in [2, 4]:

            return 'ground'

        elif obj.target_category == 3:

            return 'maritime'


class CombatLogTimeSeriesSerializer(serializers.Serializer):

    kills = serializers.IntegerField()
    date = serializers.DateField()
