from rest_framework.permissions import BasePermission


def get_role_name(user):
    role = getattr(user, 'role', None)
    if hasattr(role, 'name'):
        return role.name
    return (role or '').lower()


class EsAdministrador(BasePermission):
    """Solo permite acceso a usuarios con rol 'administrador'."""
    message = 'Acceso denegado. Se requiere rol de administrador.'

    def has_permission(self, request, view):
        role_name = get_role_name(request.user)
        return bool(
            request.user and
            request.user.is_authenticated and
            role_name in ['admin', 'administrador']
        )


class EsMecanicoOAdmin(BasePermission):
    """Permite acceso a mecánicos y administradores."""
    def has_permission(self, request, view):
        role_name = get_role_name(request.user)
        return bool(
            request.user and
            request.user.is_authenticated and
            role_name in ['mechanic', 'mecanico', 'administrador', 'admin']
        )
