from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import SFP005, SFPDXX25
from .serializers import CargosSerializer, FuncoesSerializer


# Create your views here.
@csrf_exempt
def Cargos(request):
    cargos = []
    if request.method == 'GET':
        entidade_id = request.GET.get('entidade_id')
        search = request.GET.get('search')
        for cargo in SFP005.objects.filter(entidade_id=entidade_id, cargo__icontains=search).distinct().order_by(
                'cargo'):
            dados = {}
            dados['id'] = cargo.id
            dados['text'] = cargo.codigo + '-' + cargo.cargo
            cargos.append(dados)
        return JsonResponse(data=cargos, safe=False)
    return JsonResponse(data=cargos, safe=False)


# def Cargos2(request):
#     cargos2 = []
#     if request.method == 'GET':
#         entidade_id = request.GET.get('entidade_id')
#         search = request.GET.get('search')
#         for cargo2 in SFP005.objects.filter(entidade_id=entidade_id, cargo__icontains=search).distinct().order_by(
#                 'cargo'):
#             dados = {}
#             dados['id'] = cargo2.id
#             dados['text'] = cargo2.cargo
#             cargos2.append(dados)
#         return JsonResponse(data=cargos2, safe=False)
#     return JsonResponse(data=cargos2, safe=False)

class CargosViewSet(ReadOnlyModelViewSet):
    queryset = SFP005.objects.all()
    serializer_class = CargosSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('entidade', 'codigo',)
    search_fields = ('cargo', )


class FuncoesViewSet(ReadOnlyModelViewSet):
    queryset = SFPDXX25.objects.all().order_by('cargo2')
    serializer_class = FuncoesSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = None
    filterset_fields = ('entidade', 'codigo',)
    search_fields = ('cargo2', )