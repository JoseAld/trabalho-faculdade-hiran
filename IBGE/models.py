from django.db import models


# Create your models here.
class Uf(models.Model):
    uf = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.uf)

    class Meta:
        db_table = 'uf'


class Municipios(models.Model):
    codibge = models.IntegerField()
    municipio = models.CharField(max_length=100, null=True, blank=True)
    uf = models.ForeignKey('IBGE.Uf', on_delete=models.PROTECT)

    def __str__(self):
        return '{}'.format(self.municipio)

    class Meta:
        db_table = 'municipios'
