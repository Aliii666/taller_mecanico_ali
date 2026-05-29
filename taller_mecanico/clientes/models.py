from django.db import models


class Cliente(models.Model):
    nombre    = models.CharField(max_length=100)
    telefono  = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    correo    = models.EmailField(max_length=100, blank=True, null=True)

    class Meta:
        db_table        = 'clientes'
        verbose_name    = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering        = ['nombre']

    def __str__(self):
        return self.nombre
