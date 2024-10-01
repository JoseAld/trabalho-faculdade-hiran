from rest_framework.routers import DefaultRouter
router = DefaultRouter(trailing_slash=False)

from .views import StorageViewSet

router.register('storage', StorageViewSet, basename='storage')
