from django.db import models


class DCSServer(models.Model):

    """
    This model represents a DCS server that has connected to this system
    and is providing a websocket feed
    """

    name = models.CharField(max_length=128)
    mission = models.CharField(max_length=1024)
    theatre = models.CharField(max_length=1024)
    start_time = models.DateTimeField()
    password = models.CharField(max_length=1024, null=True, blank=True)
    connection_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
