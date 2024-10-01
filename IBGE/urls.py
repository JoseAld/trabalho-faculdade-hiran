from django.urls import path
from .views import Cidades, Cep, UfViewSet, MunicipiosViewSet
from storage.urls import router

urlpatterns = [
    path('cidades/', Cidades, name="listagem_cidades"),
    path('bairros/', Cep, name="listagem_bairros"),
]

router.register('uf', UfViewSet, basename='uf')
router.register('municipio', MunicipiosViewSet, basename='municipio')
