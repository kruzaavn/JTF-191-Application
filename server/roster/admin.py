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
    pass


@admin.register(Operation)
class HQAdmin(admin.ModelAdmin):
    pass


@admin.register(Aviator)
class HQAdmin(admin.ModelAdmin):
    pass
