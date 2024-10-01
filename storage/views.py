from rest_framework import viewsets
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Storage
from .serializers import StorageSerializer


class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ('id',)
    pagination_class = None

    def get_queryset(self):
        return Storage.objects.filter(usuario=self.request._user, chave_acesso=self.request.query_params['chave_acesso'])

    def delete(self, request, *args, **kwargs):
        itens = self.get_queryset()
        self.perform_destroy(itens)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, itens):
        itens.delete()

