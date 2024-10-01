from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from banco.models import TipoConta, Bancos
from banco.serializers import BancosSerializer, TipoContaSerializer


@csrf_exempt
def BuscarTipoConta(request):
    tiposconta = []
    if request.method == 'GET':
        id = request.GET.get('id')
        search = request.GET.get('search')
        for tipoconta in TipoConta.objects.filter(codbanco=id, descricao__icontains=search).distinct():
            dados = {}
            dados['id'] = tipoconta.id
            dados['text'] = tipoconta.descricao
            tiposconta.append(dados)
        return JsonResponse(data=tiposconta, safe=False)
    return JsonResponse(data=tiposconta, safe=False)


class BancoViewSet(ReadOnlyModelViewSet):
    queryset = Bancos.objects.all()
    serializer_class = BancosSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('codbanco', 'banco',)
    search_fields = ('codbanco', '^banco',)


class TipoContaViewSet(ReadOnlyModelViewSet):
    queryset = TipoConta.objects.all().order_by('tipoconta')
    serializer_class = TipoContaSerializer
    pagination_class = None
    filterset_fields = ('codbanco', 'tipoconta', 'descricao',)