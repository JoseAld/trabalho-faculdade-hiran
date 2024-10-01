from django.db.models import Prefetch
from rest_framework import serializers
from storage.models import Storage
from usuarios.models import Usuario
from entidades.models import Entidade


class StorageMixin(object):
    def storage(self, usuario_id):
        try:
            return Storage.objects.prefetch_related(
                Prefetch('entidade',
                         queryset=Entidade.objects.order_by('razao'), to_attr='entidadelst')) \
                .prefetch_related(
                Prefetch('usuario',
                         queryset=Usuario.objects.order_by('nome'), to_attr='usuariolst')) \
                .get(usuario_id=usuario_id)
        except:
            raise serializers.ValidationError('Storage não encontrado.')

