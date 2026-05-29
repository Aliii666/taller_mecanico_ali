from rest_framework import serializers
from taller_mecanico.clientes.serializers import ClienteSerializer
from .models import Vehiculo


class VehiculoSerializer(serializers.ModelSerializer):
    cliente_detalle = ClienteSerializer(source='cliente', read_only=True)

    class Meta:
        model  = Vehiculo
        fields = ['id', 'cliente', 'cliente_detalle', 'marca', 'modelo', 'placa', 'anio']
