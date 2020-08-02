from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
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
            serializer.save()

            subject = f'{serializer.validated_data.get("callsign")} Thanks for submitting a request to join JTF-191'
            message = f'{serializer.validated_data.get("first_name")} thanks for your submission a recruiter will be ' \
                      f'in contact shortly'
            recipient = serializer.validated_data.get("email")

            send_mail(
                subject,
                message,
                'noreply@jtf191.com',
                [recipient]
            )

            subject = f'New Application from {serializer.validated_data.get("callsign")}'
            message = f'{serializer.validated_data}'
            recruiters = User.objects.filter(groups__name='Recruit')

            send_mail(subject, message, 'noreply@jtf191.com', [x.email for x in recruiters])

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
