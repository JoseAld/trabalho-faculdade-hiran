from .models import SFPD9924
from rest_framework import serializers


class UnidadesTrabSerializer(serializers.ModelSerializer):
    class Meta:
        model = SFPD9924
        fields = '__all__'