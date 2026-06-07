from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from taller_mecanico.permissions import EsAdministrador
from .models import Servicio
from .serializers import ServicioSerializer


class ServicioViewSet(viewsets.ModelViewSet):
    queryset         = Servicio.objects.all()
    serializer_class = ServicioSerializer
    search_fields    = ['nombre', 'descripcion']

    def get_permissions(self):
        # Solo admin puede crear, editar y eliminar servicios
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [EsAdministrador()]
        return [IsAuthenticated()]
