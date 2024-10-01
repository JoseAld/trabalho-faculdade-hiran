from django.urls import path, include
from .views import HomeView, EntidadeModalView, TrocaEntidadeView

app_name = 'home'
urlpatterns = [
    path('index/', HomeView.as_view(), name='Home'),
    path('modais/entidades/', EntidadeModalView.as_view(), name='selecionar_entidade'),
    path('trocar/entidades/', TrocaEntidadeView.as_view(), name='trocar_entidade'),
]
