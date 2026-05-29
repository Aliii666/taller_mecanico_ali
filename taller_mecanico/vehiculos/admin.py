from django.contrib import admin
from .models import Vehiculo

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display  = ['marca', 'modelo', 'placa', 'anio', 'cliente']
    search_fields = ['placa', 'marca', 'modelo']
    list_filter   = ['marca']
