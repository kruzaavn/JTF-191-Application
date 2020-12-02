from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from datetime import datetime, date


class HQ(models.Model):
    """
    hq table
    """
    # constants
    services = ['navy', 'marine', 'air force']
    rank_table = {
        services[0]: {i + 1: x for i, x in
                      enumerate(["ENS", "LTJG", "LT", "LCDR", "CDR", "CAPT"])},
        services[1]: {i + 1: x for i, x in enumerate(
            ["2ndLt", "1stLt", "Capt", "Maj", "LtCol", "Col"])},
        services[2]: {i + 1: x for i, x in enumerate(
            ["2nd Lt", "1st Lt", "Capt", "Maj", "Lt Col", "Col"])},
    }

    position_table = {
        services[0]: {i + 1: x for i, x in
                      enumerate(["CO", "XO", "OPSO", ""])},
        services[1]: {i + 1: x for i, x in
                      enumerate(["CO", "XO", "OPSO", ""])},
        services[2]: {i + 1: x for i, x in
                      enumerate(["CO", "XO", "OPSO", ""])},

    }

    # fields
    name = models.CharField(max_length=1024)
    service = models.CharField(choices=[(x, x) for x in services],
                               default=services[0], max_length=16)
    img = models.ImageField(upload_to='hqs')

    @property
    def service_rank_table(self):
        return self.rank_table[str(self.service)]

    @property
    def service_position_table(self):
        return self.position_table[str(self.service)]

    def __str__(self):
        return f'{self.name}'


class DCSModules(models.Model):
    module_types = ['aircraft', 'map']
    services = ['navy', 'air force']

    name = models.CharField(max_length=64)
    module_type = models.CharField(max_length=64,
                                   choices=[(x, x) for x in module_types],
                                   default=module_types[0])

    service = models.CharField(choices=[(x, x) for x in services], blank=True, null=True, max_length=64)

    def __str__(self):
        return self.name


class Squadron(models.Model):
    """
    squadron table
    """

    types = ['operational', 'replacement', 'training']

    # fields
    name = models.CharField(max_length=1024)
    designation = models.CharField(max_length=1024)
    type = models.CharField(max_length=1024, choices=[(x, x) for x in types],
                            default=types[0])
    air_frame = models.ForeignKey(DCSModules, on_delete=models.SET_NULL,
                                  blank=True, null=True)
    hq = models.ForeignKey(HQ, on_delete=models.SET_NULL, blank=True,
                           null=True)
    img = models.ImageField(upload_to='squadrons')
    callsign = models.CharField(max_length=1024, default='None')
    tri_code = models.CharField(max_length=3, default='NCS')

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


class Pilot(models.Model):
    first_name = models.CharField(max_length=1024, default='John')
    last_name = models.CharField(max_length=1024, default='Doe')
    dcs_modules = models.ManyToManyField(DCSModules, blank=True)
    callsign = models.CharField(max_length=1024)
    email = models.EmailField(max_length=1024, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.callsign}'


def stats_default():
    return {"hours": {}, "kills": {}}


class QualificationModule(models.Model):
    """
    qualification modules table


    this table tracks qualification modules tracking module documentation and checkoff periodicity
    """

    documentation_types = ['document', 'slides', 'spreadsheet', 'video']

    name = models.CharField(max_length=1024)
    link = models.URLField(max_length=2048)
    documentation_type = models.CharField(choices=[(x, x) for x in documentation_types],
                                          default=documentation_types[0],
                                          max_length=1024
                                          )
    recertification_time = models.DurationField(blank=True, null=True, help_text='DD HH:MM:SS')

    def __str__(self):
        return self.name


class Qualification(models.Model):
    """
    qualifications table

    This table tracks all modules that make up any particular qualification.
    """

    name = models.CharField(max_length=1024)
    modules = models.ManyToManyField(QualificationModule, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Aviator(Pilot):
    """
    aviator table inherits from abstract pilot table

    this table keep tracks of members who have joined the task force
    """

    # constants
    statuses = ['active', 'extended loa', 'reserve']
    positions = ['co', 'xo', 'opso', '']
    rank_helper = {i + 1: f'O-{i + 1}' for i, x in enumerate(range(6))}
    position_helper = {i + 1: x for i, x in enumerate(positions)}

    # fields
    squadron = models.ForeignKey(Squadron, on_delete=models.SET_NULL,
                                 blank=True, null=True)
    pilot = models.BooleanField(default=True)
    date_joined = models.DateField(default=datetime.now)
    status = models.CharField(choices=[(x, x) for x in statuses],
                              default=statuses[0], max_length=128)
    operations = models.ManyToManyField(Operation, blank=True)
    rank_code = models.IntegerField(default=1,
                                    validators=[MinValueValidator(1),
                                                MaxValueValidator(6)],
                                    help_text=f'{rank_helper}')
    tail_number = models.CharField(max_length=64, blank=True, null=True)
    position_code = models.IntegerField(default=4,
                                        validators=[MinValueValidator(1),
                                                    MaxValueValidator(4)],
                                        help_text=f'{position_helper}')
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.CASCADE)
    stats = models.JSONField(default=stats_default)
    division = models.IntegerField(default=4, validators=[MinValueValidator(1),
                                                          MaxValueValidator(
                                                              4)])
    division_position = models.IntegerField(default=4,
                                            validators=[MinValueValidator(1),
                                                        MaxValueValidator(4)])

    qualifications = models.ManyToManyField(Qualification, blank=True)

    @property
    def rank(self):
        if self.squadron:
            return self.squadron.hq.service_rank_table[self.rank_code]
        else:
            return

    @property
    def position(self):

        if self.squadron:
            return self.squadron.hq.service_position_table[self.position_code]
        else:
            return


class QualificationCheckoff(models.Model):
    """

    qualification checkoff table


    this table tracks the status of individual checkoffs
    """
    module = models.ForeignKey(QualificationModule, on_delete=models.CASCADE)
    aviator = models.ForeignKey(Aviator, on_delete=models.CASCADE)
    sign_off = models.ForeignKey(Aviator, on_delete=models.SET_NULL, blank=True, null=True, related_name='sign_off')
    date = models.DateField(auto_now_add=True)

    @property
    def current(self):
        if self.module.self.module.recertification_time:
            return date.today() <= self.date + self.module.recertification_time
        else:
            return True


class ProspectiveAviator(Pilot):
    """
    prospective aviator table inherits from abstract pilot table

    this table keeps track of prospective members to the task force
    """

    statuses = ['pending', 'accepted', 'rejected']

    discord = models.CharField(max_length=1024, blank=True, null=True)
    head_tracking = models.CharField(max_length=1024, default='Track IR')
    hotas = models.CharField(max_length=1024, default='x52')
    about = models.TextField(blank=True, null=True)
    submitted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=[(x, x) for x in statuses],
                              default=statuses[0],
                              max_length=64)
    preferred_airframe = models.ForeignKey(DCSModules,
                                           null=True,
                                           on_delete=models.SET_NULL,
                                           related_name='preferred_airframe')

    def create_aviator(self):

        squadron = Squadron.objects.get(
            type='training',
            hq__service=self.preferred_airframe.service
        )

        self.status = 'accepted'
        self.save()

        aviator = Aviator.objects.get_or_create(
            first_name=self.first_name,
            last_name=self.last_name,
            callsign=self.callsign,
            email=self.email,
            squadron=squadron,
        )
        dcs_modules = [x for x in self.dcs_modules]

        aviator.dcs_modules.add(*dcs_modules)
        return aviator


    def recruitment_email(self):
        return f"""Recruitment application submitted by {self.callsign} on {self.submitted.strftime("%m/%d/%y")}
                        Email: {self.email}
                        Airframe: {self.preferred_airframe.name}
                        HOTAS: {self.hotas}
                        Tracking: {self.head_tracking}
                        Discord: {self.discord}
                        About: {self.about}"""


class Event(models.Model):
    """
    event table

    this table tracks scheduled events
    """

    types = ['operation', 'training', 'admin']

    start = models.DateTimeField()
    end = models.DateTimeField()
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    required_squadrons = models.ManyToManyField(Squadron, blank=True)
    type = models.CharField(default=types[0], max_length=1024,
                            choices=[(x, x) for x in types])

    def __str___(self):
        return f'{self.name}'
