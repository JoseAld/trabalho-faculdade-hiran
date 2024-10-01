from django.db import models


class UsuarioEntidade(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.PROTECT)
    entidade = models.ForeignKey('entidades.Entidade', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.usuario} - {self.entidade}'
