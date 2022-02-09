from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, BaseValidator
from django.contrib.auth.models import User
from datetime import datetime, date
import jsonschema
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import os

def stats_default():
    return {"hours": {}, "kills": {}}


class HQ(models.Model):
    """
    hq table
    """
    # constants
    services = ['navy', 'marine', 'air force', 'army']
    rank_table = {
        services[0]: {i - 4: x for i, x in enumerate(
            ["WO1", "CW2", "CW3", "CW4", "CW5", "ENS", "LTJG", "LT", "LCDR", "CDR", "CAPT"])},
        services[1]: {i - 4: x for i, x in enumerate(
            ["WO1", "CW2", "CW3", "CW4", "CW5", "2ndLt", "1stLt", "Capt", "Maj", "LtCol", "Col"])},
        services[2]: {i - 4: x for i, x in enumerate(
            ["WO1", "CW2", "CW3", "CW4", "CW5", "2nd Lt", "1st Lt", "Capt", "Maj", "Lt Col", "Col"])},
        services[3]: {i - 4: x for i, x in enumerate(
            ["WO1", "CW2", "CW3", "CW4", "CW5", "2LT", "1LT", "CPT", "MAJ", "LTC", "COL"])},
    }

    position_table = {
        services[0]: {i + 1: x for i, x in
                      enumerate(["CO", "XO", "OPSO", ""])},
        services[1]: {i + 1: x for i, x in
                      enumerate(["CO", "XO", "OPSO", ""])},
        services[2]: {i + 1: x for i, x in
                      enumerate(["CO", "XO", "OPSO", ""])},
        services[3]: {i + 1: x for i, x in
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
    services = ['navy', 'air force', 'army']

    name = models.CharField(max_length=64, blank=True, null=True)  # human read able name
    dcs_type_name = models.CharField(max_length=1024, blank=True, null=True)
    dcs_display_name = models.CharField(max_length=1024, blank=True, null=True)

    module_type = models.CharField(max_length=64,
                                   choices=[(x, x) for x in module_types],
                                   default=module_types[0])

    service = models.CharField(choices=[(x, x) for x in services],
                               blank=True,
                               null=True,
                               max_length=64)

    def __str__(self):

        if self.name:
            return self.name
        else:
            return f'DCS {self.dcs_type_name}'


class Squadron(models.Model):
    """
    squadron table
    """

    types = ['operational', 'training']

    # fields
    name = models.CharField(max_length=1024)
    designation = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=1024, choices=[(x, x) for x in types],
                            default=types[0])
    air_frame = models.ForeignKey(DCSModules, on_delete=models.SET_NULL,
                                  blank=True, null=True)
    hq = models.ForeignKey(HQ, on_delete=models.SET_NULL, blank=True,
                           null=True)
    img = models.ImageField(upload_to='squadrons')
    callsign = models.CharField(max_length=1024, default='None')
    tri_code = models.CharField(max_length=3, default='NCS', unique=True)
    discord_channel = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.designation}'


class Operation(models.Model):
    """
    operation table
    """

    default_notes = """Use this space to disseminate essential information for the operation. 

The following items can be added similar to how you would include them in a word document. 

1. Plain text notes
2. links to mission files like [.miz][miz] and [.liberation][lib] or [briefings][brief]
3. Images
4. Tables
5. Lists and Task Checkoffs

See markdown basic syntax [here](https://www.markdownguide.org/cheat-sheet/).

[miz]: https://drive.google.com/file/d/1T99VR88fjwkEvNaWvzLIoY5uPVG9tzKY/view?usp=sharing
[lib]: https://drive.google.com/file/d/1AgS7_KbdpgZRAyPEdVObkKnYcyiAByQX/view?usp=sharing
[brief]: https://docs.google.com/presentation/d/1EmJxUxc5rK06voa4q9uANF9KX6SwvGBG-DHZTfD-HWM/edit?usp=sharing"""


    name = models.CharField(max_length=1024)
    img = models.ImageField(upload_to='operations')
    start = models.DateField()
    complete = models.DateField()
    notes = models.TextField(default=default_notes)

    def __str__(self):
        return f'{self.name}'


class Munition(models.Model):

    types = ['rocket', 'bomb', 'aa_missile', 'as_missile', 'utility', 'gun']

    name = models.CharField(max_length=1024)  # DCS Display name for now
    munition_type = models.CharField(max_length=1024, choices=[(x, x) for x in types], default=types[0])

    def __str__(self):
        return f'{self.name}'


class Stores(models.Model):

    class Meta:
        verbose_name_plural = 'Stores'

    munition = models.ForeignKey(Munition, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    squadron = models.ForeignKey(Squadron, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.munition.name}'


class Pilot(models.Model):
    first_name = models.CharField(max_length=1024, default='John')
    last_name = models.CharField(max_length=1024, default='Doe')
    dcs_modules = models.ManyToManyField(DCSModules, blank=True)
    callsign = models.CharField(max_length=1024, blank=True, null=True)
    email = models.EmailField(max_length=1024, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.callsign}'


class DocumentationModule(models.Model):
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


class Documentation(models.Model):
    """
    qualifications table

    This table tracks all modules that make up any particular qualification.
    """

    class Meta:
        verbose_name_plural = 'Documentation'

    name = models.CharField(max_length=1024)
    modules = models.ManyToManyField(DocumentationModule, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Award(models.Model):
    """
    Model for the awards' ribbons

    """
    name = models.CharField(max_length=512, blank=False, null=True)
    ribbon_image = models.FileField(upload_to='awards', blank=True, null=True, unique=True)
    priority = models.IntegerField(blank=False, null=False, unique=False, default=999)

    def __str__(self):
        return f'{self.name}'


class Aviator(Pilot):
    """
    aviator table inherits from abstract pilot table

    this table keep tracks of members who have joined the task force
    """

    # constants
    statuses = ['active', 'extended loa', 'reserve']
    positions = ['co', 'xo', 'opso', '']
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
                                    validators=[MinValueValidator(-4),
                                                MaxValueValidator(6)],
                                    )
    tail_number = models.CharField(max_length=64, blank=True, null=True)
    position_code = models.IntegerField(default=4,
                                        validators=[MinValueValidator(1),
                                                    MaxValueValidator(4)],
                                        help_text=f'{position_helper}')

    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL)

    division = models.IntegerField(default=4, validators=[MinValueValidator(1),
                                                          MaxValueValidator(
                                                              4)])
    division_position = models.IntegerField(default=4,
                                            validators=[MinValueValidator(1),
                                                        MaxValueValidator(4)])

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


class Citation(models.Model):
    """
    model for tracking when awards are given out
    """

    aviator = models.ForeignKey('Aviator', related_name='citations', on_delete=models.CASCADE)
    operation = models.ForeignKey('Operation', on_delete=models.SET_NULL, blank=True, null=True)
    award = models.ForeignKey('Award', on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.award}, {self.operation}'


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

        aviator, created = Aviator.objects.get_or_create(
            first_name=self.first_name,
            last_name=self.last_name,
            callsign=self.callsign,
            email=self.email,
            squadron=squadron,
        )

        if created:
            dcs_modules = [x for x in self.dcs_modules.all()]

            aviator.dcs_modules.add(*dcs_modules)
            aviator.save()

        return aviator


class Event(models.Model):
    """
    event table

    this table tracks scheduled events
    """

    types = ['operation', 'training', 'admin', 'leave of absence']

    start = models.DateTimeField()
    end = models.DateTimeField()
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    required_squadrons = models.ManyToManyField(Squadron, blank=True)
    aviator = models.ForeignKey('Aviator', blank=True, null=True, on_delete=models.CASCADE)
    type = models.CharField(default=types[0], max_length=1024,
                            choices=[(x, x) for x in types])

    def __str___(self):
        return f'{self.name}'


class UserImage(models.Model):

    file = models.ImageField('user_images', blank=True, null=True)
    url = models.URLField(blank=True, null=True, unique=True)
    display = models.BooleanField(default=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.file.name or self.url}'


class LiveryLuaSection (models.Model):
    name = models.CharField(max_length=128)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class LiverySkinJsonValidator(BaseValidator):
    def compare(self, value, schema):
        try:
            jsonschema.validate(value, schema)
        except jsonschema.exceptions.ValidationError as error:
            raise ValidationError(error)


class LiverySkin(models.Model):
    JSON_FIELD_SCHEMA = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "array",
        "items": [
            {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "integer",
                        "description": "X axis for the positioning of the text"
                    },
                    "y": {
                        "type": "integer",
                        "description": "Y axis for the positioning of the text"
                    },
                    "font": {
                        "type": "string",
                        "description": "The font of the text. Please ask the admin for a list of allowed fonts"
                    },
                    "prop": {
                        "type": "string",
                        "description": "The name of the property to display. This is linked to the Aviator model in DCS. The only exception is 'rankFullName', which is a custom allowed field."
                    },
                    "angle": {
                        "type": "integer",
                        "description": "this is the angle to which the text will be rotated. Default is 0"
                    },
                    "img_size": {
                        "type": "object",
                        "properties": {
                            "width": {
                                "type": "integer",
                                "description": "Width of the image that will contain the text"
                            },
                            "height": {
                                "type": "integer",
                                "description": "Height of the image that will contain the text"
                            }
                        },
                        "required": [
                            "width",
                            "height"
                        ]
                    },
                    "font_size": {
                        "type": "integer",
                        "description": "Font size of the custom text"
                    },
                    "font_opacity": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1,
                        "description": "Opacity of the custom text. Must be between 0 and 1"
                    },
                    "text_offset_x": {
                        "type": "integer",
                        "description": "Spacing of custom text within its image, X axis"
                    },
                    "text_offset_y": {
                        "type": "integer",
                        "description": "Spacing of custom text within its image, Y axis"
                    },
                    "font_alignment": {
                        "type": "string",
                        "description": "Alignment of custom text. I.e., center, left, right"
                    }
                },
                "required": [
                    "x",
                    "y",
                    "prop",
                    "img_size",
                    "text_offset_x",
                    "text_offset_y"
                ]
            }
        ]
    }
    name = models.CharField(max_length=128)
    dds_file = models.FileField(upload_to='livery_dds')
    json_description = models.JSONField(
        blank=True,
        null=True,
        validators=[LiverySkinJsonValidator(limit_value=JSON_FIELD_SCHEMA)]
    )

    # Allows for overwrites of the existing dds_file with the same name
    # As they are referenced in the Lua file an need to be consistent
    def save(self, *args, **kwargs):
        try:
            this = LiverySkin.objects.get(id=self.id)

            # Avoid deleting when there is no new file
            # i.e. clicking save without uploading a new one
            if this.dds_file and self.dds_file != this.dds_file:
                this.dds_file.storage.delete(this.dds_file.name)
        except ObjectDoesNotExist:
            pass
        super(LiverySkin, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Livery(models.Model):

    squadron = models.ForeignKey(Squadron, on_delete=models.CASCADE)
    positions = Aviator.positions
    position_helper = Aviator.position_helper
    position_code = models.IntegerField(default=4,
                                        validators=[MinValueValidator(1),
                                                    MaxValueValidator(4)],
                                        help_text=f'{position_helper}')
    skins = models.ManyToManyField(LiverySkin, blank=True)
    lua_sections = models.ManyToManyField(LiveryLuaSection, blank=True)

    def __str__(self):
        return f"{self.squadron.name} {self.positions[self.position_code - 1]}"


class Target(models.Model):

    name = models.CharField(max_length=1024, blank=True, null=True)
    dcs_type_name = models.CharField(max_length=1024, blank=True, null=True)
    dcs_display_name = models.CharField(max_length=1024, blank=True, null=True)
    category = models.IntegerField(default=0)

    @property
    def type(self):

        if self.category in [0, 1]:

            return 'air'

        elif self.category in [2, 4]:

            return 'ground'

        elif self.category == 3:

            return 'maritime'

    def __str__(self):
        if self.name:
            return f'{self.name}'
        else:
            return f'DCS {self.dcs_type_name}'


class StatsLog(models.Model):

    roles = ['pilot', 'flight crew']

    aviator = models.ForeignKey(Aviator, on_delete=models.CASCADE)
    role = models.CharField(max_length=64, default=roles[0], choices=[(x, x) for x in roles])
    time = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    altitude = models.FloatField(blank=True, null=True)
    platform = models.ForeignKey(DCSModules, on_delete=models.SET_NULL, null=True, blank=True)
    server = models.CharField(max_length=1024, null=True, blank=True)
    flight_id = models.UUIDField(editable=False, blank=True, null=True)
    mission = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.flight_id}'


class CombatLog(StatsLog):

    types = ['kill']

    target_latitude = models.FloatField(blank=True, null=True)
    target_longitude = models.FloatField(blank=True, null=True)
    target_altitude = models.FloatField(blank=True, null=True)
    munition = models.ForeignKey(Munition, on_delete=models.SET_NULL, null=True, blank=True)
    target = models.ForeignKey(Target, on_delete=models.CASCADE)
    type = models.CharField(max_length=64, default=types[0], choices=[(x, x) for x in types])


class FlightLog(StatsLog):

    types = ['takeoff', 'landing', 'pilot_death', 'ejection', 'trap']

    base = models.CharField(max_length=64, blank=True, null=True)
    grade = models.CharField(max_length=1024, blank=True, null=True)
    type = models.CharField(max_length=64, default=types[0], choices=[(x, x) for x in types])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['aviator', 'flight_id', 'type'], name='unique_log_by_id_type_aviator')
        ]

    def __str__(self):
        return f'{self.flight_id}'
