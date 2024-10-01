from django.contrib import admin
from .models import SFP005, SFPDXX25


class SFP005Admin(admin.ModelAdmin):
    list_display = ('codigo', 'cargo', 'entidade',)
    ordering = ['codigo']
    list_filter = ('entidade',)


admin.site.register(SFP005, SFP005Admin)


class SFPDXX25Admin(admin.ModelAdmin):
    list_filter = ('entidade',)


admin.site.register(SFPDXX25, SFPDXX25Admin)
