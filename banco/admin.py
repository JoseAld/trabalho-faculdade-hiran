from django.contrib import admin
from .models import Bancos, TipoConta


# Register your models here.
class BancoAdmin(admin.ModelAdmin):
    list_display = ('banco', 'codbanco',)
    ordering = ['banco']
    list_filter = ('banco',)


admin.site.register(Bancos, BancoAdmin)


class TipoContaAdmin(admin.ModelAdmin):
    list_display = ('codbanco', 'tipoconta', 'descricao',)
    ordering = ['codbanco', 'tipoconta']
    list_filter = ('descricao',)


admin.site.register(TipoConta, TipoContaAdmin)
