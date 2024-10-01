from rest_framework import serializers
from collections import OrderedDict

from .models import Storage
from usuarios.models import UsuarioEntidade


class StorageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storage
        fields = '__all__'

    def validate(self, attrs):
        request = self.context['request']

        attrs['usuario'] = request._user if request._user else None
        attrs['usuario_entidade'] = request.data['usuario_entidade'] if request.data.get('usuario_entidade', None) else None

        return attrs

    def create(self, validated_data):
        try:
            instance = Storage.objects.get(usuario=validated_data['usuario'])
        except:
            instance = None

        if not instance:
            instance = Storage()

        if validated_data['usuario_entidade']:
            instance.entidade = UsuarioEntidade.objects.get(id=validated_data['usuario_entidade']).entidade
        else:
            usuarios_entidade = UsuarioEntidade.objects.filter(usuario=validated_data['usuario'])
            if usuarios_entidade.count() == 1:
                instance.entidade = usuarios_entidade.first().entidade

        instance.usuario = validated_data.get('usuario', None)
        instance.chave_acesso = validated_data.get('chave_acesso', None)

        instance.save()

        return instance

    def to_representation(self, instance):
        ret = OrderedDict()
        ret['usuario'] = OrderedDict()
        ret['usuario']['nome'] = instance.usuario.username
        ret['usuario']['id'] = instance.usuario.id
        ret['usuario_entidade'] = OrderedDict()
        ret['usuario_entidade']['id'] = instance.entidade.id
        ret['usuario_entidade']['razao_social'] = instance.entidade.razao
        ret['usuario_entidade']['uf'] = instance.entidade.estado
        return ret
