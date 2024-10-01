from .models import SFP001, Curso, sfp017, Dependentes, Fotos
from rest_framework import serializers


class SFP001Serializer(serializers.ModelSerializer):
    class Meta:
        model = SFP001
        exclude = ['registro']


class FotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fotos
        fields = '__all__'


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'


class Sfp017Serializer(serializers.ModelSerializer):
    class Meta:
        model = sfp017
        fields = '__all__'


class DependenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependentes
        fields = '__all__'