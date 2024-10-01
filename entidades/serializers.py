from rest_framework.serializers import ModelSerializer
from entidades.models import Entidade


class EntidadeSerializer(ModelSerializer):

    class Meta:
        model = Entidade
        fields = ['id', 'cnpj', 'razao', 'estado']
