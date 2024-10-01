from django.contrib import admin
from .models import Usuario


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_full_name', 'entidades',)
    ordering = ['username']
    search_fields = ('first_name', 'username',)


admin.site.register(Usuario, UsuarioAdmin)
admin.site.enable_nav_sidebar = False
