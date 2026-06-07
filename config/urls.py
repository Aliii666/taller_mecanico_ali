from django.contrib import admin
from django.urls import path, include
from django.db import connection
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from taller_mecanico.usuarios.views import LoginView, RegistroView, MeView

@api_view(['GET'])
def api_root(request):
    return Response({
        "name": "API Taller Mecánico",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "admin": "/admin/",
            "auth": {
                "register": "/api/auth/register/",
                "login": "/api/auth/login/",
                "token_refresh": "/api/auth/token/refresh/",
                "me": "/api/auth/me/"
            },
            "clientes": "/api/clientes/",
            "vehiculos": "/api/vehiculos/",
            "servicios": "/api/servicios/",
            "ordenes": "/api/ordenes/",
            "facturas": "/api/facturas/",
            "pagos": "/api/pagos/",
            "health": "/api/health"
        }
    })

@api_view(['GET'])
def health_check(request):
    try:
        connection.ensure_connection()
        return Response({
            "status": "healthy",
            "database": "connected",
            "message": "API is running and database connection is active."
        })
    except Exception as e:
        return Response({
            "status": "unhealthy",
            "database": f"error: {str(e)}",
            "message": "Database connection failed."
        }, status=500)

urlpatterns = [
    # ── Root and Health ───────────────────────────────
    path('', api_root, name='api_root_home'),
    path('api/', api_root, name='api_root'),
    path('api/health', health_check, name='health_check'),


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
