from rest_framework.permissions import BasePermission


class EsAdministrador(BasePermission):
    """Solo permite acceso a usuarios con rol 'administrador'."""
    message = 'Acceso denegado. Se requiere rol de administrador.'

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'administrador'
        )


class EsMecanicoOAdmin(BasePermission):
    """Permite acceso a mecánicos y administradores."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role in ['mecanico', 'administrador']
        )
