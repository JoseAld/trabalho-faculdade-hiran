from django.contrib import admin
from .models import UsuarioEntidade


class UsuarioEntidadeAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'entidade',)
    list_filter = ('entidade',)


admin.site.register(UsuarioEntidade, UsuarioEntidadeAdmin)
