import pprint
import zipfile
import os

from io import BytesIO
from datetime import date, datetime, time
from django.core.mail import send_mail
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework import permissions, authentication
from django.core.exceptions import ObjectDoesNotExist

from azure.storage.blob import BlockBlobService

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError

from .models import Aviator, Livery, Squadron, HQ, DCSModules, ProspectiveAviator, Event, DocumentationModule, \
    Documentation, UserImage, Munition, Stores, Operation, FlightLog, CombatLog, \
    Target

from .serializers import AviatorSerializer, CombatLogAggregateSerializer, SquadronSerializer, HQSerializer, \
    DCSModuleSerializer, ProspectiveAviatorSerializer, EventSerializer, DocumentationSerializer, \
    DocumentationModuleSerializer, UserSerializer, UserRegisterSerializer, \
    EventCreateSerializer, MunitionSerializer, StoresSerializer, UserImageSerializer, OperationSerializer, \
    TargetSerializer, FlightLogSerializer, FlightLogAggregateSerializer, FlightLogTimeSeriesSerializer, \
    CombatLogSerializer, CombatLogTimeSeriesSerializer

from .jobs import create_aviator_dds, create_aviator_lua


class AviatorListView(ListCreateAPIView):

    serializer_class = AviatorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Aviator.objects.all().order_by('-rank_code', 'position_code')


class AviatorFromUserListView(RetrieveUpdateDestroyAPIView):

    serializer_class = AviatorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'user_id'
    def get_queryset(self):
        return Aviator.objects.filter(user__id=self.kwargs["user_id"])


class AviatorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Aviator.objects.all()
    serializer_class = AviatorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        aviator = Aviator.objects.get(pk=kwargs['aviator_id'])
        if aviator.user:
            return Response({'detail': ['Aviator has already been registered']},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        model = serializer.create(serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        aviator.user = model
        aviator.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SquadronListView(ListCreateAPIView):
    queryset = Squadron.objects.all()
    serializer_class = SquadronSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class HQListView(ListCreateAPIView):
    queryset = HQ.objects.all()
    serializer_class = HQSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DCSModuleListView(ListCreateAPIView):
    queryset = DCSModules.objects.all()
    serializer_class = DCSModuleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProspectiveAviatorDetailView(CreateAPIView):
    queryset = ProspectiveAviator.objects.all()
    serializer_class = ProspectiveAviatorSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            prospective = serializer.save()

            subject = 'Thanks for submitting a request to join JTF-191'
            html = render_to_string('recruitment.html', {'prospective': prospective}).replace("\n", "")
            message = strip_tags(html)
            recipient = prospective.email

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [recipient],
                html_message=html
            )

            subject = f'New Application from {prospective.callsign}'
            html = render_to_string('recruitment_notification.html', {'prospective': prospective}).replace("\n", "")
            message = strip_tags(html)
            leaders = Aviator.objects.filter(position_code__lt=4)
            admins = User.objects.filter(is_superuser=True)

            send_mail(subject,
                      message,
                      settings.EMAIL_HOST_USER,
                      [x.email for x in leaders if x.email] + [x.email for x in admins if x.email],
                      html_message=html
                      )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatsView(APIView):

    authentication_classes = list()

    def post(self, request, format=None):
        event_type = request.data.get('event')

        if event_type in FlightLog.types:


            try:
                self.create_flight_log(request, event_type)

                return Response(status=status.HTTP_201_CREATED)

            except (IntegrityError, ValidationError) as e:

                return Response(status=status.HTTP_208_ALREADY_REPORTED)

        elif event_type in CombatLog.types:


            self.create_combat_log(request, event_type)

            return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def create_flight_log(self, request, event_type):

        pilot, flight_crew = self.get_pilot_and_crew(request.data.get('crew'))
        platform = self.get_platform(request.data.get('unit'))

        FlightLog.objects.create(
            aviator=pilot,
            role='pilot',
            latitude=request.data.get('latitude'),
            longitude=request.data.get('longitude'),
            altitude=request.data.get('altitude'),
            platform=platform,
            server=request.data.get('server'),
            flight_id=request.data.get('flight_id'),
            mission=request.data.get('mission'),
            base=request.data.get('place', dict()).get('displayName'),
            grade=request.data.get('comment'),
            type=event_type
        )

        for crew in flight_crew:

            FlightLog.objects.create(
                aviator=crew,
                role='flight crew',
                latitude=request.data.get('latitude'),
                longitude=request.data.get('longitude'),
                altitude=request.data.get('altitude'),
                platform=platform,
                server=request.data.get('server'),
                flight_id=request.data.get('flight_id'),
                mission=request.data.get('mission'),
                base=request.data.get('place', dict()).get('displayName'),
                grade=request.data.get('comment'),
                type=event_type
            )

    def create_combat_log(self, request, event_type):

        pilot, flight_crew = self.get_pilot_and_crew(request.data.get('crew'))
        platform = self.get_platform(request.data.get('unit'))
        target = self.get_target(request.data.get('target'))
        munition = self.get_munition(request.data.get('munition'))

        CombatLog.objects.create(
            aviator=pilot,
            role='pilot',
            latitude=request.data.get('latitude'),
            longitude=request.data.get('longitude'),
            altitude=request.data.get('altitude'),
            platform=platform,
            server=request.data.get('server'),
            flight_id=request.data.get('flight_id'),
            mission=request.data.get('mission'),
            target_latitude=request.data.get('target_latitude'),
            target_longitude=request.data.get('target_longitude'),
            target_altitude=request.data.get('target_alt'),
            munition=munition,
            target=target,
            type=event_type
        )

        for crew in flight_crew:

            CombatLog.objects.create(
                aviator=crew,
                role='flight crew',
                latitude=request.data.get('latitude'),
                longitude=request.data.get('longitude'),
                altitude=request.data.get('altitude'),
                platform=platform,
                server=request.data.get('server'),
                flight_id=request.data.get('flight_id'),
                mission=request.data.get('mission'),
                target_latitude=request.data.get('target_latitude'),
                target_longitude=request.data.get('target_longitude'),
                target_altitude=request.data.get('target_altitude'),
                munition=munition,
                target=target,
                type=event_type
            )

    def get_platform(self, unit):

        platform, created = DCSModules.objects.get_or_create(
            dcs_type_name=unit.get('typeName'),
            dcs_display_name=unit.get('displayName')
        )

        return platform

    def get_munition(self, weapon):

        if weapon:
            munition, created = Munition.objects.get_or_create(
                name=weapon
            )

            return munition
        else:
            return None

    def get_target(self, unit):

        print(pprint.pprint(unit), flush=True)

        target, created = Target.objects.get_or_create(
            dcs_type_name=unit.get('typeName'),
            dcs_display_name=unit.get('displayName'),
            category=unit.get('category')
        )

        return target

    def get_pilot_and_crew(self, crew):

        pilot_callsign = crew['pilot'].split('|')[1].strip()
        flight_crew_callsigns = [x.split('|')[1].strip() for x in crew['flight_crew']]

        pilot = Aviator.objects.get(callsign=pilot_callsign)
        flight_crew = Aviator.objects.filter(callsign__in=flight_crew_callsigns)

        return pilot, flight_crew


class StoresView(APIView):

    authentication_classes = list()

    def post(self, request, format=None):

        stores_case = {
            'takeoff': -1,
            'landing': 1
        }

        event = request.data

        print(event, flush=True)

        callsign = event.get('callsign')

        tri_code = event.get('name')[:3].upper()

        try:
            squadron = Squadron.objects.get(tri_code=tri_code)

        except ObjectDoesNotExist:
            squadron = None

        if squadron:

            operation = Operation.objects.last()

            for store in event.get('stores'):

                munition, created = Munition.objects.get_or_create(name=store['name'])

                new_store = Stores(squadron=squadron,
                                   operation=operation,
                                   count=store['count'] * stores_case[event['event']],
                                   munition=munition)

                new_store.save()

            return Response(status=status.HTTP_202_ACCEPTED)

        else:

            return Response(status=status.HTTP_400_BAD_REQUEST)


class EventListView(ListCreateAPIView):

    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if 'start' in self.kwargs and 'end' in self.kwargs:
            start = self.kwargs['start']
            end = self.kwargs['end']
            return Event.objects.filter(start__gte=start, end__lte=end)
        return Event.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            model = serializer.create(serializer.validated_data)
            output_serializer = EventSerializer(model)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            model = serializer.update(self.get_object(), serializer.validated_data)
            output_serializer = EventSerializer(model)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QualificationListView(ListCreateAPIView):

    queryset = Documentation.objects.all()
    serializer_class = DocumentationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class QualificationDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Documentation.objects.all()
    serializer_class = DocumentationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class QualificationModuleListView(ListCreateAPIView):

    queryset = DocumentationModule.objects.all()
    serializer_class = DocumentationModuleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class QualificationModuleDetailView(RetrieveUpdateDestroyAPIView):

    queryset = DocumentationModule.objects.all()
    serializer_class = DocumentationModuleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserImageListView(ListCreateAPIView):
    queryset = UserImage.objects.filter(display=True).order_by('-datetime')
    serializer_class = UserImageSerializer
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MunitionListView(ListCreateAPIView):
    queryset = Munition.objects.all()
    serializer_class = MunitionSerializer


class StoresListView(ListCreateAPIView):

    serializer_class = StoresSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):

        return Stores.objects.filter(operation__name=self.kwargs.get('name'))


class OperationListView(ListCreateAPIView):
    queryset = Operation.objects.all().order_by('-start')
    serializer_class = OperationSerializer


class AviatorLiveriesListView(ListCreateAPIView):
    # The livery generation permissions will only be for admins
    # Get calls will be for all logged in users and return the files from blob
    permission_classes = [permissions.IsAuthenticated]
    azure_key = "A0Q1yZMbSMgj8qs+snYcFk9uhynJSF1FoR9KmG5LAAiPTp7bYYRYYvXKdCdW+vq9j/NaZOaKsQpg0kIHNlqjKA=="#os.getenv('AZURE_STORAGE_KEY')
    account_name = 'jtf191blobstoragedev'
    azure_container = 'static'

    block_blob_service = BlockBlobService(account_name=account_name, account_key=azure_key)

    def get(self, request):
        blobs = self.block_blob_service.list_blobs(container_name=self.azure_container, prefix="livery/")
        archive = BytesIO()
        with zipfile.ZipFile(archive, 'w') as zip_file:
            for blob in blobs:
                file = self.block_blob_service.get_blob_to_bytes(
                        container_name=self.azure_container,
                        blob_name=blob.name)
                zip_file.writestr(blob.name, file.content)

        response = HttpResponse(archive.getvalue(), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="%s"' % 'liveries.zip'
        return response

    def post(self, request):
        """
        Steps:
        - Get all aviators
        - Per aviator:
            - Get Position
            - Get Squadron
            - Per Airframe
                - Get liveries from Blob based on the above props
                - Get Skin details from Django
                - Create DDS and LUA files
                - Upload those to Blob
        """
        if not request.user.is_staff:
            return Response({'detail': ['Not allowed']},
                            status=status.HTTP_403_FORBIDDEN)

        aviators = Aviator.objects.all()
        if not aviators:
            return Response({'detail': ['No Aviators found']},
                            status=status.HTTP_404_NOT_FOUND)

        for aviator in aviators:
            squadron = aviator.squadron.designation

            # This is needed as DCS needs a very specific name for each airframe
            airframe_dcs_name = aviator.squadron.air_frame.dcs_type_name
            if not airframe_dcs_name:
                # we skip this airframe as it doesn't have the type name set
                continue

            # Get liveries from DB
            squadron_livery = Livery.objects.filter(squadron__designation = squadron)\
                    .filter(position_code = aviator.position_code).first()
            if not squadron_livery:
                # No livery for current position
                # If position is not base, try defaulting to base (4) if present
                squadron_livery = Livery.objects.filter(squadron__designation = squadron)\
                    .filter(position_code = 4).first()

                if not squadron_livery:
                    # not base livery set for this airframe, skipping
                    continue

            # Get all the livery's skins
            skins = squadron_livery.skins.all()
            
            # Create custom DDS file for aviator and save in blob storage
            for skin in skins:
                file_name = os.path.basename(skin.dds_file.name)
                dds_path = f"livery/{airframe_dcs_name}/{squadron} {aviator.callsign}/{file_name}"
                create_aviator_dds.delay(skin, aviator, dds_path)

            lua_path = f"livery/{airframe_dcs_name}/{squadron} {aviator.callsign}/description.lua"
            lua_sections = squadron_livery.lua_sections.all()
            create_aviator_lua.delay(aviator,lua_sections, lua_path)
           
        return Response({'detail': "Complete"}, status=status.HTTP_201_CREATED)


class TargetListView(ListAPIView):

    queryset = Target.objects.all()
    serializer_class = TargetSerializer


class FlightLogListView(ListAPIView):

    serializer_class = FlightLogSerializer

    def get_queryset(self):

        aviator = Aviator.objects.get(id=self.kwargs['aviator_pk'])

        return FlightLog.objects.filter(aviator=aviator)


class CombatLogListView(ListAPIView):

    serializer_class = CombatLogSerializer

    def get_queryset(self):

        aviator = Aviator.objects.get(id=self.kwargs['aviator_pk'])

        return CombatLog.objects.filter(aviator=aviator)


class FlightLogAggregateView(ListAPIView):

    serializer_class = FlightLogAggregateSerializer

    def get_queryset(self):

        sql_query = '''
                    with flights as (
                        select 
                            MAX(time) - MIN(time) as flight_time, 
                            flight_id, 
                            platform_id, 
                            aviator_id 
                        from 
                            roster_flightlog 
                        where 
                            aviator_id=%s 
                        group by 
                            flight_id, 
                            platform_id, 
                            aviator_id
                            )   select 
                                    SUM(flight_time) as total_flight_time, 
                                    1 as id, 
                                    platform_id 
                                from 
                                    flights 
                                group by 
                                    platform_id;'''

        logs = FlightLog.objects.raw(sql_query, [self.kwargs['aviator_pk']])
        return logs


class FlightLogTimeSeriesView(ListAPIView):

    serializer_class = FlightLogTimeSeriesSerializer

    def get_queryset(self):

        if not self.kwargs['time_span']:

            sql_query = """
                        with flights as (
                            select 
                                Max(time) - Min(time) as flight_time, 
                                Date(Min(time)) as date 
                            from 
                                roster_flightlog 
                            where 
                                aviator_id=%s 
                            group by 
                                flight_id
                            )   select 
                                    SUM(flight_time) as total_flight_time, 
                                    date, 
                                    1 as id 
                                from 
                                    flights 
                                group by 
                                    date
                                order by
                                    date ASC; """

            logs = FlightLog.objects.raw(sql_query, [self.kwargs['aviator_pk']])

        else:

            sql_query = """
                        with flights as (
                            select 
                                Max(time) - Min(time) as flight_time, 
                                Date(Min(time)) as date 
                            from 
                                roster_flightlog 
                            where 
                                aviator_id=%s 
                            group by 
                                flight_id
                            )   select 
                                    SUM(flight_time) as total_flight_time, 
                                    date, 
                                    1 as id 
                                from 
                                    flights 
                                where 
                                    date >= current_date - %s
                                group by 
                                    date
                                order by
                                    date ASC; """

            logs = FlightLog.objects.raw(sql_query, [self.kwargs['aviator_pk'], self.kwargs['time_span']])

        return logs


class CombatLogAggregateView(ListAPIView):

    serializer_class = CombatLogAggregateSerializer

    def get_queryset(self, *args, **kwargs):

        sql_query = """
                    select 
                        COUNT(category) as kills, 
                        category as target_category, 
                        1 as id 
                    from 
                        roster_combatlog 
                    inner join 
                        roster_target on roster_target.id = roster_combatlog.target_id 
                    where 
                        aviator_id=%s and type='kill' 
                    group by 
                        category; """

        logs = CombatLog.objects.raw(sql_query, [self.kwargs['aviator_pk']])

        return logs


class CombatLogTimeSeriesView(ListAPIView):

    serializer_class = CombatLogTimeSeriesSerializer

    def get_queryset(self):

        if not self.kwargs['time_span']:

            sql_query = """
                            select 
                                COUNT(type) as kills, 
                                Date(time) as date, 
                                1 as id 
                            from 
                                roster_combatlog 
                            where 
                                aviator_id=%s 
                            group by
                                date
                            order by
                                date ASC; """

            logs = CombatLog.objects.raw(sql_query, [self.kwargs['aviator_pk']])

        else:

            sql_query = """
                            select 
                                COUNT(type) as kills, 
                                Date(time) as date, 
                                1 as id 
                            from 
                                roster_combatlog 
                            where 
                                aviator_id=%s and date >= current_date - %s
                            group by
                                date
                            order by
                                date ASC; """

            logs = CombatLog.objects.raw(sql_query, [self.kwargs['aviator_pk'], self.kwargs['time_span']])

        return logs
