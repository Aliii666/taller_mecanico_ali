from django.db import migrations, models


ROLE_NAMES = ['admin', 'mechanic', 'client']


def seed_roles(apps, schema_editor):
    Role = apps.get_model('usuarios', 'Role')
    for role_name in ROLE_NAMES:
        Role.objects.get_or_create(name=role_name)


def unseed_roles(apps, schema_editor):
    Role = apps.get_model('usuarios', 'Role')
    Role.objects.filter(name__in=ROLE_NAMES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'db_table': 'roles',
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, default='', max_length=100)),
                ('last_name', models.CharField(blank=True, default='', max_length=100)),
                ('avatar_url', models.URLField(blank=True, null=True)),
                ('timezone', models.CharField(default='America/Guayaquil', max_length=100)),
                ('user', models.OneToOneField(on_delete=models.deletion.CASCADE, related_name='profile', to='usuarios.usuario')),
            ],
            options={
                'db_table': 'user_profiles',
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
        migrations.RunPython(seed_roles, unseed_roles),
    ]
