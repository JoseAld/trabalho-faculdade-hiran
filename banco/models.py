from django.db import models


# Create your models here.
class Bancos(models.Model):
    codbanco = models.CharField(max_length=3, null=True, blank=True)
    banco = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.codbanco)

    class Meta:
        db_table = 'bancos'


class TipoConta(models.Model):
    codbanco = models.ForeignKey('banco.Bancos', null=True, blank=True, on_delete=models.PROTECT)
    tipoconta = models.CharField(max_length=3, null=True, blank=True)
    descricao = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.descricao)

    class Meta:
        db_table = 'tipoconta'
