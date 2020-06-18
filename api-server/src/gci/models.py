from django.db import models


class DCSServer(models.Model):

    """This model represents a DCS server that has connected to this system and is providing a websocket feed"""

    name = models.CharField(max_length=128)
    ip = models.GenericIPAddressField()
    connection_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
