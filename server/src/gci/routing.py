from django.urls import re_path

from .consumers import GCIConsumer

websocket_urlpatterns = [
    re_path(r'ws/gci/$', GCIConsumer),
]
