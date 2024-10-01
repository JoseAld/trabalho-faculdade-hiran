from banco.models import Bancos, TipoConta
from rest_framework import serializers


class BancosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bancos
        fields = '__all__'


class TipoContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoConta
        fields = '__all__'

