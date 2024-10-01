from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from SFP006.models import SFP006
from SFP006.serializers import LotacoesSerializer


@csrf_exempt
def Secretarias(request):
    secretarias = []
    if request.method == 'GET':
        entidade_id = request.GET.get('entidade_id')
        search = request.GET.get('search')
        for secretaria in SFP006.objects.filter(entidade_id=entidade_id, descricao__icontains=search).distinct().order_by('descricao'):
            dados = {}
            dados['id'] = secretaria.id
            dados['text'] = secretaria.cdsecreta + '-' + secretaria.descricao
            secretarias.append(dados)
        return JsonResponse(data=secretarias, safe=False)
    return JsonResponse(data=secretarias, safe=False)

@csrf_exempt
def Setores(request):
    setores = []
    if request.method == 'GET':
        entidade_id = request.GET.get('entidade_id')
        search = request.GET.get('search')
        for setor in SFP006.objects.filter(entidade_id=entidade_id, descricao__icontains=search).distinct().order_by('descricao'):
            dados = {}
            dados['id'] = setor.id
            dados['text'] = setor.cdsetor + '-' + setor.descricao
            setores.append(dados)
        return JsonResponse(data=setores, safe=False)
    return JsonResponse(data=setores, safe=False)


class LotacoesViewSet(ReadOnlyModelViewSet):
    queryset = SFP006.objects.all().order_by('cdsecreta', 'cdsetor')
    serializer_class = LotacoesSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('entidade', 'cdsecreta', 'cdsetor',)
    search_fields = ('descricao', )
