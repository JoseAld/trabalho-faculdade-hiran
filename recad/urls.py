from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt import views as jwt_views
from usuarios.views import CustonLoginView
from django.conf import settings
from django.conf.urls.static import static
from home.views import handler500

from storage.urls import router as base
from entidades.urls import router as entidade
from usuarios.urls import router as usuarios
from banco.urls import router as banco
from IBGE.urls import router as ibge
from controle.urls import router as controle
from SFP005.urls import router as cargo
from SFP006.urls import router as lotacoes
from SFP001.urls import router as pessoa

urlpatterns = [
                path('admin/', admin.site.urls),
                path('api/', include(base.urls)),
                path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
                path('api/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

                path('', CustonLoginView.as_view(), name="inicio"),
                path('usuarios/', include('usuarios.urls')),
                path('controle/', include('controle.urls')),
                path('SFP001/', include('SFP001.urls')),
                path('entidades/', include('entidades.urls')),
                path('usuario/entidades/', include('usuario_entidade.urls')),
                path('home/', include('home.urls')),
                path('ibge/', include('IBGE.urls')),
                path('banco/', include('banco.urls')),
                path('CFG_VINC/', include('CFG_VINC.urls')),
                path('SFP005/', include('SFP005.urls')),
                path('SFP006/', include('SFP006.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler500 = handler500