from rest_framework import viewsets, serializers
from storage.models import Storage


class BaseModelViewSet(viewsets.ModelViewSet):
    _storage = None

    def storage(self):
        try:
            self._storage = Storage.objects.get(usuario_id=self.request.user.id)
        except Storage.DoesNotExist:
            self._storage = None
            raise serializers.ValidationError('Storage não encontrado.')

        return self._storage

    def get_queryset(self):
        queryset = super(BaseModelViewSet, self).get_queryset()

        kwargs = {}
        if 'entidade' in self.queryset.model.__dict__:
            kwargs['entidade'] = self.storage().entidade

        qs_vigentes = queryset.filter(**kwargs)

        return qs_vigentes


class EntidadeModelViewSet(viewsets.ModelViewSet):
    _storage = None

    def storage(self):
        try:
            self._storage = Storage.objects.get(usuario_id=self.request.user.id)
        except Storage.DoesNotExist:
            self._storage = None
            raise serializers.ValidationError('Storage não encontrado.')
        except AttributeError:
            self._storage = None
            raise serializers.ValidationError('Storage não encontrado.')

        return self._storage

    def get_queryset(self):
        queryset = super(EntidadeModelViewSet, self).get_queryset()

        kwargs = {}
        if 'entidade' in self.queryset.model.__dict__:
            kwargs['entidade'] = self.storage().entidade

        qs_vigentes = queryset.filter(**kwargs)

        return qs_vigentes
