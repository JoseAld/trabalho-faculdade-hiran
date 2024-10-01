from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, ListView, DetailView

from core.views.basic_views import BasicCreateView, PermissaoMixin, EntidadeMixin, BasicDetailView
from core.views.viewset import EntidadeModelViewSet
from storage.models import Storage
from usuario_entidade.models import UsuarioEntidade
from .forms import EntidadeForm
from .models import Entidade
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers
from .serializers import EntidadeSerializer


class NovaEntidade(LoginRequiredMixin, PermissaoMixin, BasicCreateView):
    form_class = EntidadeForm
    template_name = 'entidade/cadastro.html'
    success_url = reverse_lazy('entidades:cadastro_entidade')

    # def post(self, *args, **kwargs):
    #     form = self.form_class(self.request.POST, self.request.FILES)
    #     if form.is_valid():
    #         form.instance.entidade_ativo = True
    #         form.save()
    #         return HttpResponseRedirect(reverse('entidades:cadastro_entidade'),
    #                                     {'messages': messages.success(self.request, 'Entidade cadastrada com sucesso')})
    #     else:
    #         return HttpResponseRedirect(reverse('entidades:cadastro_entidade'),
    #                                     {'messages': messages.error(self.request, 'Não foi possivel cadastrar a entidades')})
    # permission_required = 'entidades.add_entidade'

    def form_valid(self, form):
        form.instance.entidade_ativo = True
        form.save()
        return HttpResponseRedirect(reverse('entidades:cadastro_entidade'),
                                             {'messages': messages.success(self.request, 'Entidade cadastrada com sucesso')})
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível cadastrar a entidade')
        return super().form_invalid(form)

    permission_required = 'entidades.add_entidade'


class ListagemView(LoginRequiredMixin, PermissaoMixin, EntidadeMixin, ListView):
    model = Entidade
    template_name = 'entidade/lista.html'
    context_object_name = 'secretaria'  # Default: object_list

    def get_queryset(self):
        return Entidade.objects.all().order_by('razao')

    permission_required = 'entidades.view_entidade'


class AtualizarEntidade(LoginRequiredMixin,BasicDetailView, UpdateView, EntidadeMixin, ):
    model = Entidade
    form_class = EntidadeForm
    template_name = 'entidade/cadastro.html'


    def form_valid(self, form):
        form.instance.entidade_ativo = True
        form.save()
        return HttpResponseRedirect(reverse('entidades:atualizar_entidade', kwargs={'pk': self.object.pk}),
                                    {'messages': messages.success(self.request, 'Entidade editada com sucesso')})
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi salvar as modificações')
        return super().form_invalid(form)

class VisualizarEntidade(LoginRequiredMixin, DetailView):
    model = Entidade
    form_class = EntidadeForm
    template_name = 'entidade/detalhe.html'
    success_url = reverse_lazy('entidades:visualizar_entidade')

    def visualizar_entidade(request, entidade_id):
        entidade = Entidade.objects.get(pk=entidade_id)
        return render(request, 'entidades/detalhe.html', {'entidade': entidade})


class SituacaoEntidadeView(LoginRequiredMixin, PermissaoMixin, UpdateView):
    model = Entidade
    form_class = EntidadeForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if self.object.entidade_ativo:
            try:
                if self.request.is_ajax():
                    self.object.entidade_ativo = False
                    self.object.save()
                    return HttpResponse(messages.success(self.request, 'Entidade desativado com sucesso!'))
            except Exception as e:
                return HttpResponse(messages.error(self.request, f'O Entidade não pode ser desativado!'))
        else:
            try:
                if self.request.is_ajax():
                    self.object.is_active = True
                    self.object.save()
                    return HttpResponse(messages.success(self.request, 'Entidade ativado com sucesso!'))
            except Exception as e:
                return HttpResponse(messages.error(self.request, 'O Entidade não pode ser ativado!'))

    permission_required = 'usuarios.change_usuario'


class EntidadeViewSet(EntidadeModelViewSet):
    queryset = Entidade.objects.all()
    serializer_class = EntidadeSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('cnpj', 'razao', )
    filterset_fields = ('cnpj', 'razao', 'id')

    def set_storage(self):
        try:
            self.storage = Storage.objects.get(usuario_id=self.request.user.id)
        except:
            raise serializers.ValidationError('Storage não encontrado.')

    def get_queryset(self):
        self.set_storage()
        return self.queryset.filter(id=self.storage.entidade_id)