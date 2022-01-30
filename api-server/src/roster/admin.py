from django.contrib import admin
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django_json_widget.widgets import JSONEditorWidget
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
    date_hierarchy = 'start'

    list_display = ('name', 'start', 'end')

    search_fields = ('start',)


@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    pass


@admin.register(DocumentationModule)
class DocumentationModuleAdmin(admin.ModelAdmin):
    pass


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
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(LiveryLuaSection)
class LiveryLuaSectionAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(FlightLog)
class FlightLogAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'

    list_display = ('flight_id', 'time', 'type', 'aviator', 'server')

    list_filter = ('aviator__squadron__designation', 'aviator__squadron__hq__name', 'server')

    search_fields = ('flight_id', 'aviator__callsign', 'server')


@admin.register(CombatLog)
class CombatLogAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'

    list_display = ('flight_id', 'time', 'type', 'aviator', 'munition', 'target', 'server')

    list_filter = ('aviator__squadron__designation', 'aviator__squadron__hq__name', 'server')

    search_fields = ('flight_id', 'aviator__callsign', 'server')


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):

    list_display = ('name', 'type')

    list_filter = ('name',)
