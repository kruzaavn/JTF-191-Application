from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView, CreateAPIView

from .models import Aviator, Squadron, HQ, DCSModules, ProspectiveAviator

from .serializers import AviatorSerializer, SquadronSerializer, HQSerializer, \
    DCSModuleSerializer, ProspectiveAviatorSerializer


class AviatorListView(ListCreateAPIView):

    queryset = Aviator.objects.all().order_by('-rank_code', 'position_code')
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


class DCSModuleListView(ListCreateAPIView):
    queryset = DCSModules.objects.all()
    serializer_class = DCSModuleSerializer


class ProspectiveAviatorDetailView(CreateAPIView):
    queryset = ProspectiveAviator.objects.all()
    serializer_class = ProspectiveAviatorSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            prospective = serializer.save()

            subject = f'{prospective.callsign} Thanks for submitting a request to join JTF-191'
            message = f'{prospective.first_name} thanks for your submission a recruiter will be ' \
                      f'in contact shortly'
            recipient = prospective.email

            send_mail(
                subject,
                message,
                'noreply@jtf191.com',
                [recipient]
            )

            subject = f'New Application from {prospective.callsign}'
            message = f'{prospective.recruitment_email()}'
            recruiters = User.objects.filter(groups__name='Recruit')

            send_mail(subject,
                      message,
                      'noreply@jtf191.com',
                      [x.email for x in recruiters]
                      )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatsView(APIView):

    """
        for tracking flight hours it is assumed that the departure key of the aviators.stats will have the correct
        airframe and simtime in second from start
    """

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

            elif event_name == 'connect':

                if aviator.stats['departure']:

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
            return Response( status=status.HTTP_400_BAD_REQUEST)