from django.urls import path, include
from storage.urls import router
from .views import NovaEntidade, ListagemView, AtualizarEntidade, VisualizarEntidade, SituacaoEntidadeView, EntidadeViewSet

app_name = 'entidades'
urlpatterns = [
    path('cadastro/', NovaEntidade.as_view(), name='cadastro_entidade'),
    path('listagem/', ListagemView.as_view(), name='listagem_entidade'),
    path('editar/<int:pk>', AtualizarEntidade.as_view(), name='atualizar_entidade'),
    path('detalhe/<int:pk>', VisualizarEntidade.as_view(), name='visualizar_entidade'),
    path('situacao/<int:pk>', SituacaoEntidadeView.as_view(), name="situacao_entidade"),
]

router.register('entidade', EntidadeViewSet, basename='entidade')