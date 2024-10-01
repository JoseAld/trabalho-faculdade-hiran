from django.db import models


# Create your models here.
class SFPD9924(models.Model):
    codigo = models.CharField(max_length=3, null=True, blank=True)
    escola = models.CharField(max_length=40, null=True, blank=True)
    obs = models.CharField(max_length=40, null=True, blank=True)
    cdsecreta = models.CharField(max_length=10, null=True, blank=True)
    entidade = models.ForeignKey('entidades.Entidade', on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.codigo)

    class Meta:
        db_table = 'sfpd9924'
        verbose_name = 'sfpdD9924'
        verbose_name_plural = 'Unidade de Trabalho'
