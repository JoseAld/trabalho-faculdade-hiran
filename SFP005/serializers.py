from .models import SFP005, SFPDXX25
from rest_framework import serializers


class CargosSerializer(serializers.ModelSerializer):
    class Meta:
        model = SFP005
        fields = '__all__'


class FuncoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SFPDXX25
        fields = '__all__'

