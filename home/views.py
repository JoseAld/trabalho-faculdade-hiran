from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
import datetime

from usuario_entidade.models import UsuarioEntidade
from entidades.models import Entidade
from SFP001.models import SFP001, RelatoriosCadastro
from core.views.basic_views import EntidadeMixin, UsuarioMixin
from entidades.models import Entidade
from usuario_entidade.models import UsuarioEntidade


def handler500(request, *args, **argv):
    response = render(None, 'admin/500.html', {})
    response.status_code = 500
    return response

def redirect_after_login(request):

    if request.user.is_superuser:
        return redirect('home:Home')
    else:
        return redirect('home:Home')


class HomeView(LoginRequiredMixin, TemplateView, EntidadeMixin, UsuarioMixin):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        entidade_selecionada = request.session.get('entidade_selecionada')

        if entidade_selecionada:
            # Se a entidade selecionada existir, redirecionar para a página principal
            return super().dispatch(request, *args, **kwargs)

        else:
            return redirect('home:selecionar_entidade')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entidades_usuario = UsuarioEntidade.objects.filter(usuario=self.request.user).count()

        hora = datetime.datetime.now()
        entidade = self.get_entidade()
        importado = SFP001.objects.filter(status='I', entidade=entidade).count()
        editado = SFP001.objects.filter(status='E', entidade=entidade).count()
        funcionario = SFP001.objects.filter(status='U', entidade=entidade).count()
        finalizado = SFP001.objects.filter(status='F', entidade=entidade).count()
        qtde_importado = [importado]
        qtde_editado = [editado]
        qtde_funcionario = [funcionario]
        qtde_finalizado = [finalizado]
        relatorios = {'qtde_importado': qtde_importado, 'qtde_editado': qtde_editado,
                      'qtde_finalizado': qtde_finalizado, 'qtde_funcionario': qtde_funcionario,
                      'importado': importado, 'editado': editado,
                      'finalizado': finalizado, 'funcionario': funcionario}
        if 6 <= hora.hour < 12:
            mensagem = "Bom dia, seja bem-vindo!"
        elif 12 <= hora.hour < 18:
            mensagem = "Boa tarde, seja bem-vindo!"
        else:
            mensagem = "Boa noite, seja bem-vindo!"
        context['mensagem'] = messages.success(self.request, str(mensagem))
        context['entidade'] = entidade.razao
        context['entidades_usuario'] = entidades_usuario
        context['entidade_id'] = entidade.id
        context['relatorios'] = relatorios
        return context

    def post(self, request):
        if self.request.is_ajax():
            return JsonResponse({"success": True}, status=200)
        return JsonResponse({"success": False}, status=400)


class EntidadeModalView (LoginRequiredMixin, TemplateView, EntidadeMixin, UsuarioMixin):
    template_name = ''
    http_methods = ['GET', 'POST']  # Permitir métodos GET e POST


    def get_context_data(self, **kwargs):
        context = super(EntidadeModalView, self).get_context_data(**kwargs)
        entidades_usuario = UsuarioEntidade.objects.filter(usuario=self.get_usuario())

        context['entidades_usuario'] = entidades_usuario
        if len(entidades_usuario) > 1:
            self.template_name = 'modais/entidades.html'
        elif len(entidades_usuario) == 1:
            self.request.session['entidade_selecionada'] = entidades_usuario[0].pk
            return redirect('home:Home')
        return context

    def post(self, request):
        try:
            request.session['entidade_selecionada'] = self.request.POST['entidade_selecionada']
            return redirect('home:Home')
        except Exception as erro:
            print(erro)
            pass
        context = self.get_context_data()
        return self.render_to_response(context)


    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.request.session.get('entidade_selecionada', None) is not None:
            return redirect('home:Home')
        return self.render_to_response(context)

class TrocaEntidadeView (LoginRequiredMixin, TemplateView, EntidadeMixin, UsuarioMixin):
    template_name = 'modais/entidades.html'
    http_methods = ['GET', 'POST']

    def get(self, request, *args, **kwargs):

        del request.session['entidade_selecionada']

        return redirect("home:Home")
