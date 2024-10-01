from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from .forms import UsuarioEntidadeForm
from .models import UsuarioEntidade
from core.views.basic_views import PermissaoMixin, BasicDeleteView, BasicCreateView


class CadastrarUsuarioEntidadeView(LoginRequiredMixin, PermissaoMixin, BasicCreateView):
    form_class = UsuarioEntidadeForm
    template_name = 'usuario_entidade/modal_usuario_entidade.html'
    permission_required = 'usuario_entidade.add_usuario_entidade'
    success_url = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.kwargs['pk']
        kwargs['entidades'] = int(self.get_entidade())
        return kwargs

    def get_success_url(self):
        return self.request.path

    def post(self, *args, **kwargs):
        if self.request.method == "POST" and self.request.is_ajax():
            form = self.form_class(**self.get_form_kwargs())
            if self.request.is_ajax():
                if form.is_valid():
                    form.instance.entidade_id = int(self.get_entidade())
                    form.instance.usuario_id = self.kwargs['pk']
                    form.save()
                    return JsonResponse({"recad": messages.success(self.request, 'Usuário vinculado no Entidade com sucesso!')}, safe=True, status=200)
                else:
                    return JsonResponse({"mensagem": messages.error(self.request, 'Usuário já vinculado a entidade!')}, status=400)

        return JsonResponse({"success": False}, status=400)


class DeletarUsuarioEntidadeView(LoginRequiredMixin, PermissaoMixin, BasicDeleteView):
    model = UsuarioEntidade
    msg_sucesso = 'Usuário foi desligado da entidade!'
    msg_erro = 'Não é possivel desligar o usuário da entidade!'
    permission_required = 'usuario_entidade.delete_usuario_entidade'
