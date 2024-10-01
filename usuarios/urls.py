from django.urls import path, include
from storage.urls import router
from .views import NovoUsuario, AtualizarUsuario, ListagemUsuario, CustonLoginView, \
    ChangePasswordView, Perfil, SituacaoUsuarioView, DesativarUsuarioView, UsuarioViewSet

app_name = 'usuarios'
urlpatterns = [
    path('login/', CustonLoginView.as_view(), name='login'),
    path('reset/senha/', ChangePasswordView.as_view(), name='resetar_senha'),
    path('perfil/', Perfil.as_view(), name="perfil"),
    path('', include('django.contrib.auth.urls')),
    path('form/', NovoUsuario.as_view(), name="cadastro_usuario"),
    path('listagem/', ListagemUsuario.as_view(), name="listagem_usuario"),
    path('edit/<int:pk>', AtualizarUsuario.as_view(), name="atualizar_usuario"),
    path('situacao/<int:pk>', SituacaoUsuarioView.as_view(), name="situacao_usuario"),
    path('desativar_usuario/<int:pk>', DesativarUsuarioView.as_view(), name="desativar_usuario")
]

router.register('usuario', UsuarioViewSet, basename='usuario')
