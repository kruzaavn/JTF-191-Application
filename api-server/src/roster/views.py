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
    QualificationModule, QualificationCheckoff, UserImage, Munition, Stores, Operation

from .serializers import AviatorSerializer, SquadronSerializer, HQSerializer, \
    DCSModuleSerializer, ProspectiveAviatorSerializer, EventSerializer, QualificationSerializer, \
    QualificationModuleSerializer, QualificationCheckoffSerializer, UserSerializer, UserRegisterSerializer, \
    EventCreateSerializer, MunitionSerializer, StoresSerializer, UserImageSerializer, OperationSerializer


stores_case = {
    'takeoff': -1,
    'landing': 1
}

class AviatorListView(ListCreateAPIView):

    serializer_class = AviatorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Aviator.objects.all().order_by('-rank_code', 'position_code')


class AviatorFromUserListView(RetrieveUpdateDestroyAPIView):

    serializer_class = AviatorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Aviator.objects.filter(user__id=self.kwargs["pk"])


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


    """
        for tracking flight hours it is assumed that the departure key of the aviators.stats will have the correct
        airframe and simtime in second from start
    """
    authentication_classes = list()

    def post(self, request, format=None):
        event_name = request.data.get('event')
        callsign = request.data.get('callsign')
        time = float(request.data.get('time'))

        if callsign:
            aviators = [x for x in Aviator.objects.all() if x.callsign.lower() in callsign.lower()]
        else:
            aviators = []

        if aviators:

            aviator = aviators[0]

            if event_name == 'takeoff':

                aviator.stats['departure'] = {'airframe': request.data.get('airframe'),
                                              'time': time}

            elif event_name == 'connect' and aviator.stats.get('departure'):

                aviator.stats.pop('departure')

            elif event_name in ['landing', 'pilot_death', 'eject', 'change_slot'] and aviator.stats.get('departure'):

                departure = aviator.stats.pop('departure')

                flight_time = (time - departure['time']) / 3600

                if departure['airframe'] in aviator.stats['hours'].keys() and flight_time > 0:
                    aviator.stats['hours'][departure['airframe']] = aviator.stats['hours'][departure['airframe']] + \
                                                                    flight_time
                elif flight_time > 0:
                    aviator.stats['hours'][departure['airframe']] = flight_time

            elif event_name in ['kill']:

                victim = request.data.get('victim')

                previous_kills = aviator.stats['kills'].get(victim, 0)

                if previous_kills and victim:
                    aviator.stats['kills'][victim] += 1

                elif victim:
                    aviator.stats['kills'][victim] = 1

            aviator.save()

            serializer = AviatorSerializer(aviator)

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

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