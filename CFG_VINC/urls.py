from django.urls import path
from .views import Vinculos

urlpatterns = [
    path('vinculos/', Vinculos, name='listagem_vinculos'),
]