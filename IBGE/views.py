from django.http import JsonResponse
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt
import pycep_correios

from IBGE.models import Municipios, Uf
from IBGE.serializers import UfSerializer, MunicipiosSerializer


@csrf_exempt
def Cidades(request):
    cidades = []
    if request.method == 'GET':
        id = request.GET.get('id')
        search = request.GET.get('search')
        for cidade in Municipios.objects.filter(uf=id, municipio__icontains=search).distinct().order_by('municipio'):
            dados = {}
            dados['id'] = cidade.id
            dados['text'] = cidade.municipio
            cidades.append(dados)
        return JsonResponse(data=cidades, safe=False)
    return JsonResponse(data=cidades, safe=False)

@csrf_exempt
def Cep(request):
    endereco = None
    if request.method == 'GET':
        search = request.GET.get('search')

        endereco = pycep_correios.consultar_cep(search)

        # print(endereco['end'])
        # print(endereco['bairro'])
        # print(endereco['cidade'])
        # print(endereco['complemento'])
        # print(endereco['complemento2'])
        # print(endereco['uf'])
        # print(endereco['cep'])

        return JsonResponse(data=endereco, safe=False)
    return JsonResponse(data=endereco, safe=False)


class UfViewSet(ReadOnlyModelViewSet):
    queryset = Uf.objects.all()
    serializer_class = UfSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('uf',)
    search_fields = ('uf',)


class MunicipiosViewSet(ReadOnlyModelViewSet):
    queryset = Municipios.objects.all().order_by('municipio')
    serializer_class = MunicipiosSerializer
    pagination_class = None
    filterset_fields = ('uf', 'municipio',)