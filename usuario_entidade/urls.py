from django.urls import path
from .views import DeletarUsuarioEntidadeView, CadastrarUsuarioEntidadeView

app_name = 'usuario_entidade'
urlpatterns = [
    path('cadastrar/<int:pk>/', CadastrarUsuarioEntidadeView.as_view(), name="cadastrar_usuario_entidade"),
    path('deletar/<int:pk>', DeletarUsuarioEntidadeView.as_view(), name='deletar_usuario_entidade'),
]