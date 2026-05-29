from django.db import models
from taller_mecanico.facturas.models import Factura


class Pago(models.Model):
    METODOS = [
        ('efectivo',     'Efectivo'),
        ('tarjeta',      'Tarjeta'),
        ('transferencia','Transferencia'),
    ]

    factura     = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='pagos')
    metodo_pago = models.CharField(max_length=20, choices=METODOS)
    monto       = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table     = 'pagos'
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering     = ['-fecha_pago']

    def __str__(self):
        return f'Pago #{self.pk} — ${self.monto} ({self.metodo_pago})'
