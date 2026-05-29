from django.db import models
from taller_mecanico.ordenes.models import OrdenTrabajo


class Factura(models.Model):
    ESTADOS_PAGO = [
        ('pendiente', 'Pendiente'),
        ('pagado',    'Pagado'),
    ]

    orden         = models.OneToOneField(OrdenTrabajo, on_delete=models.CASCADE, related_name='factura')
    total         = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    estado_pago   = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='pendiente')

    class Meta:
        db_table     = 'facturas'
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering     = ['-fecha_emision']

    def __str__(self):
        return f'Factura #{self.pk} — Orden #{self.orden_id} [{self.estado_pago}]'
