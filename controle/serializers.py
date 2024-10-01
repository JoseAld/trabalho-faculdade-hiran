from .models import Controle
from rest_framework import serializers


class ControleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Controle
        fields = '__all__'

