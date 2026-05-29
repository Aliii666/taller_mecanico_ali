from django.contrib import admin
from .models import Pago

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display  = ['id', 'factura', 'metodo_pago', 'monto', 'fecha_pago']
    list_filter   = ['metodo_pago']
