from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Pago
from .serializers import PagoSerializer


class PagoViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    Pagos: solo se pueden crear y consultar (no editar ni eliminar).
    Al crear, si el total pagado >= total factura, la factura se marca como pagada.
    """
    serializer_class   = PagoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pago.objects.select_related('factura').all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pago = serializer.save()

        # Verificar si la factura queda saldada
        factura = pago.factura
        total_pagado = sum(p.monto for p in factura.pagos.all())
        factura_pagada = False
        if total_pagado >= factura.total:
            factura.estado_pago = 'pagado'
            factura.save()
            factura_pagada = True

        return Response({
            'mensaje': 'Pago registrado exitosamente.',
            'pago': PagoSerializer(pago).data,
            'factura_saldada': factura_pagada,
        }, status=status.HTTP_201_CREATED)
