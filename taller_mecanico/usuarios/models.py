from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


ROLE_ALIASES = {
    'administrador': 'admin',
    'mecanico': 'mechanic',
    'cliente': 'client',
}


def normalize_role_name(role_name):
    role_name = (role_name or 'client').strip().lower()
    return ROLE_ALIASES.get(role_name, role_name)


class Role(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField('Usuario', on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100, blank=True, default='')
    avatar_url = models.URLField(blank=True, null=True)
    timezone = models.CharField(max_length=100, default='America/Guayaquil')

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f'Profile of {self.user.username}'


class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio.')
        email = self.normalize_email(email)
        role_name = normalize_role_name(extra_fields.pop('role', 'client'))
        user = self.model(username=username, email=email, role=role_name, **extra_fields)
        user.set_password(password)
        user.sync_flags_from_role()
        user.save(using=self._db)
        UserProfile.objects.get_or_create(user=user)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('admin', 'Admin'),
        ('mechanic', 'Mechanic'),
        ('client', 'Client'),
    ]

    username   = models.CharField(max_length=50, unique=True)
    email      = models.EmailField(max_length=100, unique=True)
    role       = models.CharField(max_length=30, choices=ROLES, default='client')
    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UsuarioManager()

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def sync_flags_from_role(self):
        role_name = normalize_role_name(self.role)
        privileged_roles = {'admin'}
        self.is_staff = role_name in privileged_roles
        self.is_superuser = role_name in privileged_roles

    def save(self, *args, **kwargs):
        self.sync_flags_from_role()
        super().save(*args, **kwargs)

    @property
    def role_object(self):
        role_name = normalize_role_name(self.role)
        role, _ = Role.objects.get_or_create(name=role_name)
        return role

    def __str__(self):
        return f'{self.username} ({normalize_role_name(self.role)})'
