from django.contrib import admin
from .models import OrdenTrabajo

@admin.register(OrdenTrabajo)
class OrdenAdmin(admin.ModelAdmin):
    list_display  = ['id', 'vehiculo', 'mecanico', 'estado', 'fecha_ingreso']
    list_filter   = ['estado']
    search_fields = ['vehiculo__placa']
