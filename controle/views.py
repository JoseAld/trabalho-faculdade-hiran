from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from controle.forms import FormSearch
from controle.models import Controle
from controle.serializers import ControleSerializer
from core.views.basic_views import BasicListView
from usuario_entidade.models import UsuarioEntidade


class ControleListView(LoginRequiredMixin, BasicListView):
    model = Controle
    template_name = 'lista_controle.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return super().get_queryset().filter(entidade=self.get_entidade(), descricao__icontains=query)
        else:
            return super().get_queryset().filter(entidade=self.get_entidade())

    def get_context_data(self, **kwargs):
        context = super(ControleListView, self).get_context_data(**kwargs)
        entidades_usuario = UsuarioEntidade.objects.filter(usuario=self.request.user).count()
        context['entidades_usuario'] = entidades_usuario
        context['form'] = FormSearch(initial={'search': self.request.GET.get('search')})
        return context


def Atualiza(request):
    if request.method == 'POST':
        vid = request.POST.get('id')
        vcampo = request.POST.get('campo')

        if vid is None or vcampo is None:
            return JsonResponse({'resp': 'não deu certo'}, safe=False)

        for controle in Controle.objects.filter(pk=vid):
            setattr(controle, vcampo, (not getattr(controle, vcampo)))
            controle.save()

        return JsonResponse({'resp': 'deu certo'}, safe=False)


class ControleViewSet(ReadOnlyModelViewSet):
    queryset = Controle.objects.all()
    serializer_class = ControleSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('entidade', 'campo',)
    search_fields = ('descricao',)

