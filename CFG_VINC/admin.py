from django.contrib import admin
from .models import CFG_VINC


class CFG_VINCAdmin(admin.ModelAdmin):
    list_display = ('id_vinculo', 'nm_vinculo', 'entidade')
    ordering = ['id_vinculo']
    list_filter = ('entidade',)


admin.site.register(CFG_VINC, CFG_VINCAdmin)
