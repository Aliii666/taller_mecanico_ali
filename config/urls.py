from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from taller_mecanico.usuarios.views import LoginView, RegistroView, MeView

urlpatterns = [
    path('admin/', admin.site.urls),

    # ── Auth ──────────────────────────────────────────
    path('api/auth/register/', RegistroView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/me/', MeView.as_view(), name='me'),

    # legacy aliases
    path('api/auth/registro/', RegistroView.as_view(), name='registro'),
    path('api/auth/perfil/', MeView.as_view(), name='perfil'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh_legacy'),

    # ── Apps ──────────────────────────────────────────
    path('api/clientes/',  include('taller_mecanico.clientes.urls')),
    path('api/vehiculos/', include('taller_mecanico.vehiculos.urls')),
    path('api/servicios/', include('taller_mecanico.servicios.urls')),
    path('api/ordenes/',   include('taller_mecanico.ordenes.urls')),
    path('api/facturas/',  include('taller_mecanico.facturas.urls')),
    path('api/pagos/',     include('taller_mecanico.pagos.urls')),
]
