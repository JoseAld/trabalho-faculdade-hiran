from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import Controle


class ControleAdmin(admin.ModelAdmin):
    list_filter = ('entidade',)


admin.site.register(Controle, ControleAdmin)
admin.site.register(Permission)