import datetime
import logging
from threading import Thread

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import DeleteView, CreateView, UpdateView, ListView, DetailView, TemplateView

from django.shortcuts import HttpResponse
from asgiref.sync import async_to_sync

from entidades.models import Entidade
from recad.settings import LINK_STATIC
from usuario_entidade.models import UsuarioEntidade


class EmailMixin():
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                        )


class ThreadEmail(Thread):
    def __init__(self, descricao, entidade):
        Thread.__init__(self)
        self.assunto = descricao
        self.entidade = entidade

    # def run(self):
    #     protocolo = Protocolo.objects.get(numero_protocolo=self.protocolo)
    #     # solicitante
    #     send_mail(
    #         'Documento anexado',
    #         f'Olá\n\nFoi anexado novo documento ao seu Protocolo de N° {self.protocolo}\n\nVocê pode consultar o andamento do seu processo através do link abaixo:\n\nhttps://protocolo.layoutsistemas.com.br/protocolo/consultar/\n\n{self.entidades}\n\nObrigado !',
    #         'protocolo@layoutsistemas.com.br',
    #         [str(protocolo.solicitante.email)],
    #     )


def email(self, email, senha, entidade):
    send_mail(
        'Senha de acesso',
        f'Olá !\n\nVocê foi cadastrado como usuário no Protocolo, segue suas credenciais:\n\nUsuário: {email}\n\nSua senha padrão é {senha}\n\nPara alterar sua senha acesse o link abaixo:\n\nhttps://protocolo.layoutsistemas.com.br/usuarios/password_reset/\n\nPara acessar o Protocolo acesse o link abaixo:\n\nhttps://protocolo.layoutsistemas.com.br\n\n{entidade}\n\nObrigado !',
        'protocolo@layoutsistemas.com.br',
        [str(email)],
    )


class UsuarioMixin():

    def get_usuario(self):
        return self.request.user.id

    def get_usuario_cpf(self):
        return self.request.user.cpf


class EntidadeMixin(UsuarioMixin):

    def get_entidade(self):
        try:
            return UsuarioEntidade.objects.get(id=int(self.request.session['entidade_selecionada'])).entidade
        except Exception as erro:
            print(erro)
            return UsuarioEntidade.objects.filter(usuario=self.request.user)


class BasicListView(EntidadeMixin, ListView):

    def get_queryset(self):
        kwargs = {}
        if getattr(self.model, 'entidade', None):
            kwargs['entidade_id'] = self.get_entidade().id
        return self.model.objects.filter(**kwargs)


    def get_context_data(self, **kwargs):
        context = super(BasicListView, self).get_context_data(**kwargs)
        entidades = UsuarioEntidade.objects.filter(usuario=self.get_usuario()).values_list('entidade', flat=True)
        context['entidade'] = self.get_entidade()
        context['entidades_usuario'] = Entidade.objects.filter(pk__in=entidades).count()
        context['link_static'] = LINK_STATIC
        return context


class BasicDetailView(EntidadeMixin, DetailView):

    def get_context_data(self, **kwargs):
        context = super(BasicDetailView, self).get_context_data(**kwargs)
        entidades = UsuarioEntidade.objects.filter(usuario=self.get_usuario()).values_list('entidade', flat=True)
        context['entidades_usuario'] = Entidade.objects.filter(pk__in=entidades).count()
        context['entidade'] = self.get_entidade().razao
        context['entidade_id'] = self.get_entidade().id
        return context


class BasicCreateModalView(EntidadeMixin, CreateView):
    data = dict()
    msg_sucesso = ''

    def get_context_data(self, **kwargs):
        context = super(BasicCreateModalView, self).get_context_data(**kwargs)
        return context

    def do_save(self, form):
        self.object = form.save()

    def form_valid(self, form):
        self.do_save(form)
        # messages.success(self.request, f'{self.msg_sucesso}')
        # return JsonResponse(self.data)

    def get(self, request, *args, **kwargs):
        self.object = None
        self.data['html_form'] = render_to_string(self.template_name, self.get_context_data(**kwargs),
                                                  request=self.request)
        return JsonResponse(self.data)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        # context = self.get_context_data(self.kwargs)
        # context['form'] = form
        # self.data['html_form'] = render_to_string(self.template_name, context, request=self.request)
        self.data = []
        return JsonResponse(self.data, safe=False)


class PermissaoMixin(PermissionRequiredMixin):
    msg_permissao = 'Você não possui permissão para acessa essa página'

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home:Home'),
                                        {'messages': messages.error(self.request, self.msg_permissao)})


class BasicDeleteView(EntidadeMixin, DeleteView):
    msg_sucesso = 'O registro foi excluido com sucesso!'
    msg_erro = 'O registro não pode ser excluído pois está em uso!'

    def get_context_data(self, **kwargs):
        context = super(BasicDeleteView, self).get_context_data(**kwargs)
        return context

    def delete(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            payload = {'delete': 'ok'}
            return HttpResponse(messages.success(self.request, f'{self.msg_sucesso}'))
        except Exception as e:
            # joga mensagem de erro
            return HttpResponse(messages.error(self.request, f'{self.msg_erro}'))


class BasicCreateView(EntidadeMixin, CreateView):
    msg_sucesso = ''

    def get_context_data(self, **kwargs):
        context = super(BasicCreateView, self).get_context_data(**kwargs)
        context['entidade'] = self.get_entidade().razao
        context['entidade_id'] = self.get_entidade().id
        return context

    def do_save(self, form):
        self.object = form.save()

    def form_valid(self, form):
        self.do_save(form)
        messages.success(self.request, f'{self.msg_sucesso}')
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class BasicUpdateView(EntidadeMixin, UpdateView):

    def get_context_data(self, **kwargs):
        context = super(BasicUpdateView, self).get_context_data(**kwargs)
        context['entidade'] = self.get_entidade().razao
        context['entidade_id'] = self.get_entidade().id
        return context

    def do_save(self, form):
        self.object = form.save()

    def form_valid(self, form):
        try:
            self.do_save(form)
        except Exception as e:
            messages.error(self.request, e)
        return super().form_valid(form)


class BasicTemplateView(EntidadeMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = super(BasicTemplateView, self).get_context_data(**kwargs)
        context['entidade'] = self.get_entidade().razao
        context['entidade_id'] = self.get_entidade().id
        return context


class GerarPDFMixin(object):
    def gerar_pdf(self, gerar_pdf=True):
        footer_template = 'base/footer.html'
        html = render_to_string(self.template_relatorio, self.get_context_data())
        if gerar_pdf == False:
            return html
        html_footer_str = render_to_string(footer_template, {'link_static': ''})
        html_footer_file = pydf.NamedTemporaryFile(suffix='.html')
        html_footer_file.write(html_footer_str.encode('utf8'))
        html_footer_file.seek(0)

        relatorio_pdf = pydf.generate_pdf(html,
                                          page_size='A4',
                                          orientation='portrait',
                                          margin_left='3mm',
                                          margin_right='3mm',
                                          margin_top='5mm',
                                          footer_html=html_footer_file.name
                                          )
        return relatorio_pdf

