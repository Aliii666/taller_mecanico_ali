from rest_framework import serializers
from taller_mecanico.facturas.models import Factura
from .models import Pago


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Pago
        fields = ['id', 'factura', 'metodo_pago', 'monto', 'fecha_pago']
        read_only_fields = ['fecha_pago']

    def validate_factura(self, factura):
        if factura.estado_pago == 'pagado':
            raise serializers.ValidationError('Esta factura ya está completamente pagada.')
        return factura

    def validate_monto(self, monto):
        if monto <= 0:
            raise serializers.ValidationError('El monto debe ser mayor a 0.')
        return monto
