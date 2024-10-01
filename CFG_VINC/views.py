from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from CFG_VINC.models import CFG_VINC


@csrf_exempt
def Vinculos(request):
    vinculos = []
    if request.method == 'GET':
        entidade_id = request.GET.get('entidade_id')
        search = request.GET.get('search')
        for vinculo in CFG_VINC.objects.filter(entidade_id=entidade_id, nm_vinculo__icontains=search).distinct().order_by('nm_vinculo'):
            dados = {}
            dados['id'] = vinculo.id
            dados['text'] = vinculo.id_vinculo + '-' + vinculo.nm_vinculo
            vinculos.append(dados)
        return JsonResponse(data=vinculos, safe=False)
    return JsonResponse(data=vinculos, safe=False)
