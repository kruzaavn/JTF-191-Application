from django.contrib import admin
from django.conf import settings
from django.core.mail import send_mail
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

def send_registration_email(aviator):

    if aviator.user is None and aviator.email:

        subject = f'{aviator.callsign} please register at JTF-191'
        message = f"""{aviator.callsign}, please register your login at the following link https://jtf191.com/#/register/{aviator.id}.
If you have any issues contact Brony on discord."""
        recipient = [aviator.email]

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient
        )


def email_registration(modeladmin, request, queryset):

    for aviator in queryset:
        send_registration_email(aviator)


email_registration.short_description = "Send Registration Email"


@admin.register(Aviator)
class AviatorAdmin(admin.ModelAdmin):

    list_display = ('callsign', 'squadron', 'position', 'rank', 'date_joined')

    list_filter = ('squadron__designation', 'squadron__hq__name')

    search_fields = ('callsign',)

    actions = [email_registration]


@admin.register(DCSModules)
class DCSModuleAdmin(admin.ModelAdmin):
    pass


def convert_to_aviator(modeladmin, request, queryset):

    for prospect in queryset:
        aviator = prospect.create_aviator()
        send_registration_email(aviator)


convert_to_aviator.short_description('Accept Prospective Aviator')


@admin.register(ProspectiveAviator)
class ProspectiveAviatorAdmin(admin.ModelAdmin):
    search_fields = ('callsign',)

    list_display = ('callsign', 'status')

    actions = [convert_to_aviator]


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
