from .models import Municipios, Uf
from rest_framework import serializers


class UfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uf
        fields = '__all__'


class MunicipiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipios
        fields = '__all__'

