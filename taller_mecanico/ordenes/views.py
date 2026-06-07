from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from taller_mecanico.permissions import EsAdministrador
from .models import OrdenTrabajo
from .serializers import OrdenTrabajoSerializer, CambioEstadoSerializer


class OrdenTrabajoViewSet(viewsets.ModelViewSet):
    serializer_class = OrdenTrabajoSerializer
    search_fields    = ['vehiculo__placa', 'vehiculo__marca', 'vehiculo__modelo', 'mecanico__username', 'vehiculo__cliente__nombre']

    def get_queryset(self):
        qs = OrdenTrabajo.objects.select_related('vehiculo__cliente', 'mecanico')
        estado = self.request.query_params.get('estado')
        if estado:
            qs = qs.filter(estado=estado)
        return qs

    def get_permissions(self):
        if self.action == 'destroy':
            return [EsAdministrador()]
        return [IsAuthenticated()]

    def destroy(self, request, *args, **kwargs):
        orden = self.get_object()
        if orden.estado != 'pendiente':
            return Response(
                {'error': 'Solo se pueden eliminar órdenes en estado pendiente.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['put'], url_path='estado')
    def cambiar_estado(self, request, pk=None):
        orden = self.get_object()
        serializer = CambioEstadoSerializer(data=request.data)
        if serializer.is_valid():
            orden.estado = serializer.validated_data['estado']
            if 'observaciones' in serializer.validated_data:
                orden.observaciones = serializer.validated_data['observaciones']
            orden.save()
            return Response({
                'mensaje': 'Estado actualizado correctamente.',
                'orden': OrdenTrabajoSerializer(orden).data,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
