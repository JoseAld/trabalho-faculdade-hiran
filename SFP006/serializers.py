from .models import SFP006
from rest_framework import serializers


class LotacoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SFP006
        fields = '__all__'
