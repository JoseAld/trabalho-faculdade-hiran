from django.db import models

from usuarios.models import Usuario
from entidades.models import Entidade


class Storage(models.Model):
    entidade = models.ForeignKey(
        Entidade, related_name='entidade_storage', null=True, blank=True, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(
        Usuario, related_name='usuario_storage', null=True, blank=True, on_delete=models.DO_NOTHING)
    chave_acesso = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'storage'
