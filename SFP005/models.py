from django.db import models

# Create your models here.
class SFP005(models.Model):
    codigo = models.CharField(max_length=3, null=True, blank=True)
    cargo = models.CharField(max_length=40, null=True, blank=True)
    entidade = models.ForeignKey('entidades.Entidade', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.codigo, self.cargo)

    class Meta:
        db_table = 'sfp005'
        verbose_name = 'SFP005'
        verbose_name_plural = 'Cargos'


class SFPDXX25(models.Model):
    codigo = models.CharField(max_length=3, null=True, blank=True)
    cargo2 = models.CharField(max_length=40, null=True, blank=True)
    entidade = models.ForeignKey('entidades.Entidade', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.codigo, self.cargo2)

    class Meta:
        db_table = 'sfpdXX25'
        verbose_name = 'sfpdXX25'
        verbose_name_plural = 'Cargos 2'
