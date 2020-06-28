from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Aviator, Squadron, HQ
from .serializers import AviatorSerializer, SquadronSerializer, HQSerializer
# Create your views here.


class AviatorListView(ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Aviator.objects.all().order_by('-rank_code', 'position_code')
    serializer_class = AviatorSerializer


class AviatorDetailView(RetrieveUpdateDestroyAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Aviator.objects.all()
    serializer_class = AviatorSerializer


class AviatorMyView(RetrieveUpdateDestroyAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AviatorSerializer

    def get_queryset(self):
        return Aviator.objects.get(user=self.request.user)


class SquadronListView(ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Squadron.objects.all()
    serializer_class = SquadronSerializer


class HQListView(ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = HQ.objects.all()
    serializer_class = HQSerializer