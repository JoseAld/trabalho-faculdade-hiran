from django.contrib import admin
from .models import SFP001, Dependentes, sfp017, Curso


class SFP001Admin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'entidade',)
    ordering = ['nome']
    search_fields = ('matricula', 'nome',)
    list_filter = ('entidade',)


admin.site.register(SFP001, SFP001Admin)


class DependentesAdmin(admin.ModelAdmin):
    list_display = ('nomedep',)
    ordering = ['nomedep']
    search_fields = ('nomedep',)


admin.site.register(Dependentes, DependentesAdmin)


class AfastamentoAdmin(admin.ModelAdmin):
    list_display = ('matricula',)
    ordering = ['matricula']
    search_fields = ('matricula',)


admin.site.register(sfp017, AfastamentoAdmin)


class CursoAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'entidade',)
    ordering = ['matricula']
    search_fields = ('matricula',)


admin.site.register(Curso, CursoAdmin)
