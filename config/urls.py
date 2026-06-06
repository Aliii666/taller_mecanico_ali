from django.contrib import admin
from django.urls import path, include
try:
    from rest_framework_simplejwt.views import TokenRefreshView
except Exception:
    from django.http import JsonResponse
    from django.views import View

    class TokenRefreshView(View):
        def post(self, request, *args, **kwargs):
            return JsonResponse({'detail': 'token refresh unavailable in this environment'}, status=501)

from taller_mecanico.usuarios.views import LoginView, RegistroView, PerfilView

urlpatterns = [
    path('admin/', admin.site.urls),

    # ── Auth ──────────────────────────────────────────
    path('api/auth/login/',    LoginView.as_view(),   name='login'),
    path('api/auth/registro/', RegistroView.as_view(), name='registro'),
    path('api/auth/perfil/',   PerfilView.as_view(),   name='perfil'),
    path('api/auth/refresh/',  TokenRefreshView.as_view(), name='token_refresh'),

    # ── Apps ──────────────────────────────────────────
    path('api/clientes/',  include('taller_mecanico.clientes.urls')),
    path('api/vehiculos/', include('taller_mecanico.vehiculos.urls')),
    path('api/servicios/', include('taller_mecanico.servicios.urls')),
    path('api/ordenes/',   include('taller_mecanico.ordenes.urls')),
    path('api/facturas/',  include('taller_mecanico.facturas.urls')),
    path('api/pagos/',     include('taller_mecanico.pagos.urls')),
]
