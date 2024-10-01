from django.contrib import admin
from .models import SFPD9924


class SFPD9924Admin(admin.ModelAdmin):
    list_display = ('codigo', 'escola', 'entidade',)
    ordering = ['codigo']
    list_filter = ('entidade',)


admin.site.register(SFPD9924, SFPD9924Admin)
