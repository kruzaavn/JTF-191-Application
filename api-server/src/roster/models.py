from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from datetime import datetime


class HQ(models.Model):

    """
    hq table
    """
    # constants
    services = ['navy', 'marine', 'air force']
    rank_table = {
        services[0]: {i + 1: x for i, x in enumerate(["ENS", "LTJG", "LT", "LCDR", "CDR", "CAPT"])},
        services[1]: {i + 1: x for i, x in enumerate(["2ndLt", "1stLt", "Capt", "Maj", "LtCol", "Col"])},
        services[2]: {i + 1: x for i, x in enumerate(["2nd Lt", "1st Lt", "Capt", "Maj", "Lt Col", "Col"])},
    }

    position_table = {
        services[0]: {i + 1: x for i, x in enumerate(["CO", "XO", "OPSO", ""])},
        services[1]: {i + 1: x for i, x in enumerate(["CO", "XO", "OPSO", ""])},
        services[2]: {i + 1: x for i, x in enumerate(["CO", "XO", "OPSO", ""])},

    }

    # fields
    name = models.CharField(max_length=1024)
    service = models.CharField(choices=[(x, x) for x in services], default=services[0], max_length=16)
    img = models.ImageField(upload_to='hqs')

    @property
    def service_rank_table(self):
        return self.rank_table[str(self.service)]


    @property
    def service_position_table(self):
        return self.position_table[str(self.service)]

    def __str__(self):
        return f'{self.name}'


class AirFrame(models.Model):

    """
    airframe table
    """

    # fields
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class Squadron(models.Model):

    """
    squadron table
    """

    types = ['operational', 'replacement', 'training']

    # fields
    name = models.CharField(max_length=1024)
    designation = models.CharField(max_length=1024)
    type = models.CharField(max_length=1024, choices=[(x, x) for x in types], default=types[0])
    air_frame = models.ForeignKey(AirFrame, on_delete=models.SET_NULL, blank=True, null=True)
    hq = models.ForeignKey(HQ, on_delete=models.SET_NULL, blank=True, null=True)
    img = models.ImageField(upload_to='squadrons')

    def __str__(self):
        return f'{self.name} - {self.designation}'


class Operation(models.Model):

    """
    operation table
    """

    name = models.CharField(max_length=1024)
    img = models.ImageField(upload_to='operations')
    start = models.DateField()
    complete = models.DateField()

    def __str__(self):
        return f'{self.name}'


class Event(models.Model):

    """
    event table
    """

    # constants
    types = ['loa', 'training', 'operation']

    type = models.CharField(max_length=48, choices=[(x, x) for x in types], default=types[0])
    start = models.DateField()
    end = models.DateField(blank=True, null=True)
    information = models.TextField()

    def __str__(self):
        return f'{self.start} - {self.type}'


class Aviator(models.Model):

    """
    aviator table
    """

    # constants
    statuses = ['active', 'extended loa', 'reserve']
    positions = ['co', 'xo', 'opso']

    # fields
    first_name = models.CharField(max_length=1024, default='John')
    last_name = models.CharField(max_length=1024, default='Doe')
    callsign = models.CharField(max_length=1024)
    squadron = models.ForeignKey(Squadron, on_delete=models.SET_NULL, blank=True, null=True)
    pilot = models.BooleanField(default=True)
    date_joined = models.DateField(default=datetime.now)
    status = models.CharField(choices=[(x, x) for x in statuses], default=statuses[0], max_length=128)
    operations = models.ManyToManyField(Operation, blank=True)
    rank_code = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(6)])
    tail_number = models.CharField(max_length=64, blank=True, null=True)
    position_code = models.IntegerField(default=4, validators=[MinValueValidator(1), MaxValueValidator(4)])
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    events = models.ManyToManyField(Event, blank=True)

    @property
    def rank(self):
        return self.squadron.hq.service_rank_table[self.rank_code]

    @property
    def position(self):
        return self.squadron.hq.service_position_table[self.position_code]

    def __str__(self):
        return f'{self.callsign}'

