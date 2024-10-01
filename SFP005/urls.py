from django.urls import path
from .views import Cargos, CargosViewSet, FuncoesViewSet
from storage.urls import router

urlpatterns = [
    path('cargos/', Cargos, name='listagem_cargos'),
    # path('cargos2/', Cargos2, name='listagem_cargos2'),
]

router.register('cargos', CargosViewSet, basename='cargos')
router.register('funcoes', FuncoesViewSet, basename='funcoes')
