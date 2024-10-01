from typing import Any
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import UsuarioEntidade, Usuario


class UsuarioEntidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioEntidade
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'username')

    def validate(self, attrs):
        request = self.context.get('request')
        senha = attrs['password']
        if request.method in ['PATCH', 'PUT']:
            if self.instance.password != senha:
                attrs['password'] = make_password(senha)
        return attrs
