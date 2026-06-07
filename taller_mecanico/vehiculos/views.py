from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from taller_mecanico.permissions import EsAdministrador
from .models import Vehiculo
from .serializers import VehiculoSerializer


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset         = Vehiculo.objects.select_related('cliente').all()
    serializer_class = VehiculoSerializer
    search_fields    = ['marca', 'modelo', 'placa', 'cliente__nombre']

    def get_permissions(self):
        if self.action == 'destroy':
            return [EsAdministrador()]
        return [IsAuthenticated()]
