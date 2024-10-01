from django.db import models


# Create your models here.
class SFP006(models.Model):
    cdsecreta = models.CharField(max_length=3, null=True, blank=True)
    cdsetor = models.CharField(max_length=3, null=True, blank=True)
    cddepart = models.CharField(max_length=3, null=True, blank=True)
    descricao = models.CharField(max_length=40, null=True, blank=True)
    entidade = models.ForeignKey('entidades.Entidade', on_delete=models.CASCADE)

    def __str__(self):
        if self.cdsetor == '000':
            return '{} - {}'.format(self.cdsecreta, self.descricao)
        else:
            return '{} - {}'.format(self.cdsetor, self.descricao)

    class Meta:
        db_table = 'sfp006'
        verbose_name = 'sfp006'
        verbose_name_plural = 'Lotacoes'
