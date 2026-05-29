from rest_framework import serializers
from taller_mecanico.ordenes.serializers import OrdenTrabajoSerializer
from .models import Factura


class FacturaSerializer(serializers.ModelSerializer):
    orden_detalle = OrdenTrabajoSerializer(source='orden', read_only=True)

    class Meta:
        model  = Factura
        fields = ['id', 'orden', 'orden_detalle', 'total', 'fecha_emision', 'estado_pago']
        read_only_fields = ['fecha_emision', 'estado_pago']

    def validate_orden(self, orden):
        if hasattr(orden, 'factura'):
            raise serializers.ValidationError('Ya existe una factura para esta orden.')
        return orden
