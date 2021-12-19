from django.contrib import admin
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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
        html = render_to_string("registration.html", {"aviator": aviator}).replace("\n", "")
        message = strip_tags(html)
        recipient = [aviator.email]

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient,
            html_message=html
        )


def email_registration(modeladmin, request, queryset):

    for aviator in queryset:
        send_registration_email(aviator)


email_registration.short_description = "Send Registration Email"


@admin.register(Aviator)
class AviatorAdmin(admin.ModelAdmin):

    list_display = ('callsign', 'user', 'squadron', 'position', 'rank', 'date_joined', 'status', )

    list_filter = ('squadron__designation', 'squadron__hq__name', 'status')

    search_fields = ('callsign', 'user__username')

    actions = [email_registration]


@admin.register(DCSModules)
class DCSModuleAdmin(admin.ModelAdmin):
    pass


def convert_to_aviator(modeladmin, request, queryset):

    for prospect in queryset:
        aviator = prospect.create_aviator()
        send_registration_email(aviator)


convert_to_aviator.short_description = 'Accept Prospective Aviator'


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


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority')


@admin.register(Citation)
class CitationAdmin(admin.ModelAdmin):
    list_display = ('aviator', 'operation', 'award')
    list_filter = ('aviator__callsign', 'operation__name', 'award__name')


@admin.register(Munition)
class MunitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'munition_type')
    list_filter = ('munition_type',)
    search_fields = ('name',)


@admin.register(Stores)
class StoresAdmin(admin.ModelAdmin):
    list_display = ('munition', 'count', 'squadron', 'operation', 'time')

    list_filter = ('munition__name', 'squadron__name', 'operation__name')


@admin.register(UserImage)
class UserImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Livery)
class LiveryAdmin(admin.ModelAdmin):

    def get_postition_from_code(self, obj):
        if obj.position_code:
            positions = ["CO", "XO", "OPSO", "BASE"]
            return positions[obj.position_code - 1]
    get_postition_from_code.short_description = 'Position'
    list_display = ('squadron', 'get_postition_from_code')


@admin.register(LiverySkin)
class LiverySkinAdmin(admin.ModelAdmin):
    list_display = ('name',)



@admin.register(LiveryLuaSection)
class LiveryLuaSectionAdmin(admin.ModelAdmin):
    list_display = ('name',)

