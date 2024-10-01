from django.urls import path
from .views import Secretarias, Setores, LotacoesViewSet
from storage.urls import router

urlpatterns = [
    path('secretarias/', Secretarias, name='listagem_secretarias'),
    path('setores/', Setores, name='listagem_setores'),
]

router.register('lotacoes', LotacoesViewSet, basename='lotacoes')