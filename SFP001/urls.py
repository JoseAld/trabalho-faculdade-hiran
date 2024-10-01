from django.urls import path, include
from storage.urls import router

from .views import ListagemPessoa, NovoPessoa, AtualizarPessoa, DeletePessoa, \
    RelatorioListaFuncionario, ImprimirRelatorioPDF, ImprimirDeclaracaoPDF, \
    SFP001ViewSet, CursoViewSet, Sfp017ViewSet, DependenteViewSet, FotoViewSet, ConfirmarPessoa

app_name = 'SFP001'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('novapessoa/', NovoPessoa.as_view(), name="cadastro_pessoa"),
    path('listagem/', ListagemPessoa.as_view(), name="listagem_pessoa"),
    path('relatorio_listafuncionario/', RelatorioListaFuncionario.as_view(), name="relatorio_listafuncionario"),
    path('editarpessoa/<int:pk>/', AtualizarPessoa.as_view(), name="atualizar_pessoa"),
    path('confirmarpessoa/<int:pk>/', ConfirmarPessoa.as_view(), name="confirmar_pessoa"),
    path('deletepessoa/<int:pk>/', DeletePessoa.as_view(), name="deletepessoa"),
    path('imprimirrelatorio/', ImprimirRelatorioPDF.as_view(), name="imprimirrelatorio"),
    path('imprimirdeclaracao/', ImprimirDeclaracaoPDF.as_view(), name="imprimirdeclaracao"),
]

router.register('pessoa', SFP001ViewSet, basename='pessoa')
router.register('foto', FotoViewSet, basename='foto')
router.register('curso', CursoViewSet, basename='curso')
router.register('afastamentos', Sfp017ViewSet, basename='afastamentos')
router.register('dependentes', DependenteViewSet, basename='dependentes')
