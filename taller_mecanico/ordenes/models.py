from django.db import models
from taller_mecanico.vehiculos.models import Vehiculo
from taller_mecanico.usuarios.models import Usuario


class OrdenTrabajo(models.Model):
    ESTADOS = [
        ('pendiente',   'Pendiente'),
        ('en_proceso',  'En proceso'),
        ('terminado',   'Terminado'),
    ]

    vehiculo      = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='ordenes')
    mecanico      = models.ForeignKey(Usuario,  on_delete=models.SET_NULL, null=True, related_name='ordenes')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    estado        = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table     = 'ordenes_trabajo'
        verbose_name = 'Orden de Trabajo'
        verbose_name_plural = 'Órdenes de Trabajo'
        ordering     = ['-fecha_ingreso']

    def __str__(self):
        return f'Orden #{self.pk} — {self.vehiculo} [{self.estado}]'
