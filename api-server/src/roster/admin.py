from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(HQ)
class HQAdmin(admin.ModelAdmin):
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

    list_filter = ('squadron__designation', 'squadron__hq__name')

    search_fields = ('callsign',)


@admin.register(DCSModules)
class DCSModuleAdmin(admin.ModelAdmin):
    pass


@admin.register(ProspectiveAviator)
class ProspectiveAviatorAdmin(admin.ModelAdmin):
    search_fields = ('callsign',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'end')

    search_fields = ('start',)


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    pass


@admin.register(QualificationModule)
class QualificationModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_requal_days')

    def get_requal_days(self, obj):
        if obj.recertification_time:
            return obj.recertification_time.days
        else:
            return None

    get_requal_days.short_description = 'Re-qualification Time'


@admin.register(QualificationCheckoff)
class QualificationCheckoffAdmin(admin.ModelAdmin):

    list_display = ('module', 'aviator', 'date', 'current')

    list_filter = ('module__name', 'aviator__callsign')
