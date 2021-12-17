from datetime import date, datetime, time
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework import permissions, authentication
from django.core.exceptions import ObjectDoesNotExist

from .models import Aviator, Squadron, HQ, DCSModules, ProspectiveAviator, Event, Qualification, \
    QualificationModule, QualificationCheckoff, UserImage, Munition, Stores, Operation, FlightLog, Kill, Target

from .serializers import AviatorSerializer, SquadronSerializer, HQSerializer, \
    DCSModuleSerializer, ProspectiveAviatorSerializer, EventSerializer, QualificationSerializer, \
    QualificationModuleSerializer, QualificationCheckoffSerializer, UserSerializer, UserRegisterSerializer, \
    EventCreateSerializer, MunitionSerializer, StoresSerializer, UserImageSerializer, OperationSerializer


stores_case = {
    'takeoff': -1,
    'landing': 1
}


class AviatorListView(ListCreateAPIView):

    queryset = Aviator.objects.all().order_by('-rank_code', 'position_code')
    serializer_class = AviatorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AviatorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Aviator.objects.all()
    serializer_class = AviatorSerializer
    permission_classes = [permissions.IsAuthenticated]


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
        callsign = request.data.get('callsign')

        aviator = Aviator.objects.filter(callsign__iexact=callsign.split('|')[1])
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        platform, created = DCSModules.objects.get_or_create(name=request.data.get('platform'))

        if aviator and event_type in FlightLog.types:

            FlightLog.objects.create(
                aviator=aviator,
                type=event_type,
                platform=platform,
                latitude=latitude,
                longitude=longitude
            )

            return Response(status=status.HTTP_201_CREATED)

        elif aviator and event_type == 'kill':

            munition, created = Munition.objects.get_or_create(name=request.data.get('munition'))
            target, created = Target.objects.get_or_create(name=request.data.get('target'))

            Kill.objects.create(
                aviator=aviator,
                latitude=latitude,
                longitude=longitude,
                altitude=request.data.get('altitude'),
                munition=munition,
                platform=platform,
                target=target
            )

            return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class StoresView(APIView):

    authentication_classes = list()

    def post(self, request, format=None):

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
        start = self.kwargs['start']
        end = self.kwargs['end']
        return Event.objects.filter(start__gte=start, end__lte=end)


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

    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class QualificationDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class QualificationModuleListView(ListCreateAPIView):

    queryset = QualificationModule.objects.all()
    serializer_class = QualificationModuleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class QualificationModuleDetailView(RetrieveUpdateDestroyAPIView):

    queryset = QualificationModule.objects.all()
    serializer_class = QualificationModuleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class QualificationCheckoffListView(ListCreateAPIView):

    queryset = QualificationCheckoff.objects.all()
    serializer_class = QualificationCheckoffSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class QualificationCheckoffDetailView(RetrieveUpdateDestroyAPIView):

    queryset = QualificationCheckoff.objects.all()
    serializer_class = QualificationCheckoffSerializer
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