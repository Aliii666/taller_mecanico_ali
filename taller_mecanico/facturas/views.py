from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Factura
from .serializers import FacturaSerializer


class FacturaViewSet(viewsets.ModelViewSet):
    serializer_class = FacturaSerializer
    http_method_names = ['get', 'post', 'head', 'options']  # Sin PUT/DELETE directo

    def get_queryset(self):
        qs = Factura.objects.select_related('orden__vehiculo__cliente')
        estado_pago = self.request.query_params.get('estado_pago')
        if estado_pago:
            qs = qs.filter(estado_pago=estado_pago)
        return qs

    def get_permissions(self):
        return [IsAuthenticated()]

    @action(detail=True, methods=['put'], url_path='marcar-pagada')
    def marcar_pagada(self, request, pk=None):
        factura = self.get_object()
        factura.estado_pago = 'pagado'
        factura.save()
        return Response({
            'mensaje': 'Factura marcada como pagada.',
            'factura': FacturaSerializer(factura).data,
        })
