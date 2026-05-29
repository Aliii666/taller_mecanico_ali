from django.contrib import admin
from .models import Factura

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'orden', 'total', 'estado_pago', 'fecha_emision']
    list_filter   = ['estado_pago']
