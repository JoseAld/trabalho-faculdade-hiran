from django.db import models

# Create your models here.
class Controle(models.Model):
    entidade = models.ForeignKey('entidades.Entidade', on_delete=models.PROTECT)
    campo = models.CharField(max_length=60)
    descricao = models.CharField(max_length=60)
    obrigatorio = models.BooleanField(default=False, null=True)
    nao_importar = models.BooleanField(default=False, null=True)
    nao_visualizar_serv = models.BooleanField(default=False, null=True)

    def __str__(self):
        return '{}'.format(self.descricao)

    class Meta:
        db_table = 'Controle'