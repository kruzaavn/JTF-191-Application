from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(HQ)
class HQAdmin(admin.ModelAdmin):
    pass


@admin.register(AirFrame)
class AirFrameAdmin(admin.ModelAdmin):
    pass


@admin.register(Squadron)
class SquadronAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'get_hq')

    def get_hq(self, obj):
        return obj.hq.name
    get_hq.short_description = 'HQ'


@admin.register(Operation)
class HQAdmin(admin.ModelAdmin):
    pass


@admin.register(Aviator)
class AviatorAdmin(admin.ModelAdmin):

    list_display = ('callsign', 'squadron', 'position', 'rank', 'date_joined')
