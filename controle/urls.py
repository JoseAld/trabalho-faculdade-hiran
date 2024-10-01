from django.urls import path, include
from .views import ControleListView, Atualiza, ControleViewSet
from storage.urls import router

app_name = 'controle'
urlpatterns = [
    path('listagem/', ControleListView.as_view(), name="listagem_controle"),
    path('atualiza/', Atualiza, name="atualiza"),
]

router.register('controle', ControleViewSet, basename='controle')