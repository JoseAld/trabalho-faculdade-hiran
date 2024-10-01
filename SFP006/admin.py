from django.contrib import admin
from .models import SFP006


class SFP006Admin(admin.ModelAdmin):
    list_display = ('cdsecreta', 'cdsetor', 'descricao', 'entidade',)
    ordering = ['cdsecreta']
    list_filter = ('entidade',)


admin.site.register(SFP006, SFP006Admin)
