from rest_framework import serializers
from taller_mecanico.vehiculos.serializers import VehiculoSerializer
from taller_mecanico.usuarios.serializers import UsuarioSerializer
from .models import OrdenTrabajo


class OrdenTrabajoSerializer(serializers.ModelSerializer):
    vehiculo_detalle = VehiculoSerializer(source='vehiculo', read_only=True)
    mecanico_detalle = UsuarioSerializer(source='mecanico',  read_only=True)

    class Meta:
        model  = OrdenTrabajo
        fields = [
            'id', 'vehiculo', 'vehiculo_detalle',
            'mecanico', 'mecanico_detalle',
            'fecha_ingreso', 'estado', 'observaciones',
        ]
        read_only_fields = ['fecha_ingreso']


class CambioEstadoSerializer(serializers.Serializer):
    ESTADOS = ['pendiente', 'en_proceso', 'terminado']
    estado        = serializers.ChoiceField(choices=ESTADOS)
    observaciones = serializers.CharField(required=False, allow_blank=True)
