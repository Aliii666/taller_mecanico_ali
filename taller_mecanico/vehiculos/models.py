from django.db import models
from taller_mecanico.clientes.models import Cliente


class Vehiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='vehiculos')
    marca   = models.CharField(max_length=50)
    modelo  = models.CharField(max_length=50)
    placa   = models.CharField(max_length=20, unique=True)
    anio    = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table     = 'vehiculos'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        ordering     = ['marca', 'modelo']

    def __str__(self):
        return f'{self.marca} {self.modelo} — {self.placa}'
