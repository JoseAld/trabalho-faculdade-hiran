from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from core.views.basic_views import EntidadeMixin, BasicCreateView, PermissaoMixin, UsuarioMixin, BasicUpdateView, \
    EmailMixin, BasicListView
from core.views.viewset import EntidadeModelViewSet
from storage.models import Storage
from usuario_entidade.models import UsuarioEntidade
from usuarios.forms import CustomAuthenticationForm, UsuarioForm
from .models import Usuario
from .serializers import UsuarioSerializer


class CustonLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = CustomAuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NovoUsuario(LoginRequiredMixin, PermissaoMixin, EmailMixin, BasicCreateView):
    form_class = UsuarioForm
    template_name = 'usuarios/cadastro.html'
    success_url = reverse_lazy('usuarios:listagem_usuario')
    permission_required = 'usuarios.add_usuario'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        usuario = form.save(commit=False)
        usuario.set_password(form.cleaned_data['password'])
        usuario.save()
        usuario.groups.set(form.cleaned_data['groups'])
        UsuarioEntidade.objects.create(usuario=usuario, entidade=self.get_entidade())
        return HttpResponseRedirect(reverse_lazy("usuarios:listagem_usuario"))


class ListagemUsuario(LoginRequiredMixin, PermissaoMixin, BasicListView):
    model = Usuario
    template_name = 'usuarios/lista.html'
    success_url = reverse_lazy('usuarios:listagem_usuario')
    permission_required = 'usuarios.view_usuario'

    def get_queryset(self):
        lista_usuario = []
        lista_usuario_entidade = UsuarioEntidade.objects.filter(entidade=self.get_entidade())
        for u in lista_usuario_entidade:
            lista_usuario.append(u.usuario.pk)
        return Usuario.objects.filter(pk__in=lista_usuario)


class Perfil(LoginRequiredMixin, EntidadeMixin,UsuarioMixin, TemplateView,):
    template_name = 'usuarios/perfil.html'

    def get_context_data(self, **kwargs):
        entidade = self.get_entidade()
        usuario = self.get_usuario()
        entidades_usuario = UsuarioEntidade.objects.filter(usuario=self.request.user).count()
        context = super(Perfil, self).get_context_data(**kwargs)
        # Contexto das informações da entidade ------>
        context['entidade'] = entidade.razao
        # context['user.cpf'] = self.get_usuario_cpf()
        context['entidade_id'] = entidade.id
        context['entidades_usuario'] = entidades_usuario
        context['entidade_fax'] = entidade.fax
        context['entidade_cnpj'] = entidade.cnpj
        context['entidade_fone'] = entidade.fone
        context['entidade_email'] = entidade.email
        context['entidade_cep'] = entidade.cep
        context['entidade_logradouro'] = entidade.logradouro
        context['entidade_log_numero'] = entidade.log_numero
        context['entidade_complemento'] = entidade.complemento
        context['entidade_bairro'] = entidade.bairro
        context['entidade_cidade'] = entidade.cidade
        return context


class AtualizarUsuario(LoginRequiredMixin, PermissaoMixin, BasicUpdateView, UsuarioMixin):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/editar.html'
    success_url = reverse_lazy('usuarios:listagem_usuario')
    permission_required = 'usuarios.change_usuario'

    def get_context_data(self, **kwargs):
        context = super(AtualizarUsuario, self).get_context_data(**kwargs)
        context['dados'] = self.object
        return context

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        usuario = form.save(commit=False)
        if self.get_object().password != form.cleaned_data['password']:
            usuario.set_password(form.cleaned_data['password'])
        usuario.save()
        usuario.groups.set(form.cleaned_data['groups'])
        return HttpResponseRedirect(reverse_lazy("usuarios:listagem_usuario"))


class SituacaoUsuarioView(LoginRequiredMixin, PermissaoMixin, BasicUpdateView):
    model = Usuario
    template_name = 'usuarios/cadastro.html'
    form_class = UsuarioForm
    permission_required = 'usuarios.change_usuario'

class ChangePasswordView(PasswordChangeView, EntidadeMixin):
    template_name = 'registration/password_change_form.html'  # Defina o nome do seu template

    def get_context_data(self, **kwargs):
        context = super(ChangePasswordView, self).get_context_data(**kwargs)
        entidades_usuario = UsuarioEntidade.objects.filter(usuario=self.request.user).count()
        context['entidade'] = self.get_entidade().razao
        context['entidade_id'] = self.get_entidade().id
        context['entidades_usuario'] = entidades_usuario
        return context

    def change_password(self, request):
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Sua senha foi alterada com sucesso!')
                return redirect('listagem_usuario')
            else:
                messages.error(request, '%s.' % PasswordChangeForm.error_messages)
        elif request.method == 'GET':
            entidade = self.get_entidade()
            form = PasswordChangeForm(request.user)
        return render(request, 'registration/password_change_form.html', {
            'entidade_id': entidade.id,
            'form': form
        })


class DesativarUsuarioView(LoginRequiredMixin, PermissaoMixin, BasicUpdateView):
    model = Usuario

    def dispatch(self, request, *args, **kwargs):
        usuario = self.get_object()
        usuario.is_active = not usuario.is_active
        usuario.save()
        return HttpResponseRedirect(reverse_lazy("usuarios:listagem_usuario"))


class UsuarioViewSet(EntidadeModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ('email',)
    search_fields = ('username',)
    ordering = ['username']

    def get_serializer_context(self):
        context = super(UsuarioViewSet, self).get_serializer_context()
        context.update({"storage": self.storage()})
        return context

    def get_queryset(self):
        usuarios_entidade = UsuarioEntidade.objects.filter(entidade=self.storage().entidade).values_list('usuario_id', flat=True)
        usuarios = Usuario.objects.filter(id__in=usuarios_entidade)
        return usuarios

    def perform_destroy(self, instance):
        UsuarioEntidade.objects.filter(entidade=self.storage().entidade,usuario=instance).delete()
        Storage.objects.filter(usuario=instance).delete()
        # instance.delete()
