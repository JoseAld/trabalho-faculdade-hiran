from django.db import models

# Create your models here.
class CFG_VINC(models.Model):
    id_vinculo = models.CharField(max_length=2, null=True, blank=True)
    nm_vinculo = models.CharField(max_length=40, null=True, blank=True)
    tribunal = models.CharField(max_length=5, null=True, blank=True)
    entidade = models.ForeignKey('entidades.Entidade', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.id_vinculo, self.nm_vinculo)

    class Meta:
        db_table = 'CFG_VINC'
        verbose_name = 'CFG_VINC'
        verbose_name_plural = 'Vinculo'