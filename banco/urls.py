from django.urls import path
from .views import BuscarTipoConta, BancoViewSet, TipoContaViewSet
from storage.urls import router

urlpatterns = [
    path('tipoconta/', BuscarTipoConta, name='listagem_tipoconta'),
]

router.register('banco', BancoViewSet, basename='banco')
router.register('tipoconta', TipoContaViewSet, basename='tipoconta')