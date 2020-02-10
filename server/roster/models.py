from django.db import models
import datetime

# Create your models here.


class HQ(models.Model):

    """
    hq table
    """
    # constants
    services = ['navy', 'marine', 'air force']
    table = {
        'navy': {i+1: x for i, x in enumerate(["ENS", "LTJG", "LT", "LCDR", "CDR", "CAPT"])},
        'marine': {i+1: x for i, x in enumerate(["2ndLt", "1stLt", "Capt", "Maj", "LtCol", "Col"])},
        'air force': {i+1: x for i, x in enumerate(["2nd Lt", "1st Lt", "Capt", "Maj", "Lt Col", "Col"])},
    }

    # fields
    name = models.CharField(max_length=1024)
    service = models.CharField(choices=[(x, x) for x in services], default=services[0], max_length=16)

    @property
    def service_table(self):
        return self.table[str(self.service)]


class AirFrame(models.Model):

    """
    airframe table
    """

    # fields
    name = models.CharField()


class Squadron(models.Model):

    """
    squadron table
    """

    # fields
    name = models.CharField(max_length=1024)
    designation = models.CharField(max_length=1024)
    air_frame = models.ForeignKey(AirFrame, on_delete=models.SET_NULL)
    hq = models.ForeignKey(HQ, on_delete=models.SET_NULL)


class Operation(models):

    """
    operation table
    """

    name = models.CharField(max_length=1024)
    img = models.ImageField(upload_to='operations')
    start = models.DateField()
    complete = models.DateField()


class Aviator(models.Model):

    """
    aviator table
    """

    # constants
    statuses = ['active', 'extended loa', 'reserve']

    # fields
    first_name = models.CharField(max_length=1024)
    last_name = models.CharField(max_length=1024)
    callsign = models.CharField(max_length=1024)
    squadron = models.ForeignKey(Squadron, on_delete=models.SET_NULL)
    pilot = models.BooleanField()
    date_joined = models.DateField()
    status = models.CharField(choices=[(x, x) for x in statuses], default=statuses[0], max_length=128)
    operations = models.ManyToManyField(Operation)
    rank_code = models.IntegerField

    @property
    def rank(self):
        return self.squadron.hq.service_table[self.rank_code]
