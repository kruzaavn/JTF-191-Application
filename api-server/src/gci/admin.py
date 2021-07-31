from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(DCSServer)
class DCSServerAdmin(admin.ModelAdmin):

    list_display = ('name', 'mission', 'theatre')
