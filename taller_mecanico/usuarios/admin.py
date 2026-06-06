from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Role, UserProfile

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display  = ['username', 'email', 'role', 'is_active', 'created_at']
    list_filter   = ['role', 'is_active']
    search_fields = ['username', 'email']
    ordering      = ['username']
    fieldsets     = (
        (None,            {'fields': ('username', 'email', 'password')}),
        ('Rol',           {'fields': ('role',)}),
        ('Permisos',      {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2', 'role')}),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'timezone']
    search_fields = ['user__username', 'user__email', 'first_name', 'last_name']
