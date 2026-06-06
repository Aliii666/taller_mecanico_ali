from django.test import TestCase
from django.contrib.auth import get_user_model

from taller_mecanico.clientes.models import Cliente
from taller_mecanico.vehiculos.models import Vehiculo
from taller_mecanico.servicios.models import Servicio
from taller_mecanico.ordenes.models import OrdenTrabajo
from taller_mecanico.facturas.models import Factura
from taller_mecanico.pagos.models import Pago


class ModelsIntegrationTest(TestCase):
    def test_create_full_flow(self):
        User = get_user_model()
        user = User.objects.create_user(username='user1', email='user1@example.com', password='pass')

        cliente = Cliente.objects.create(nombre='Cliente Test')
        vehiculo = Vehiculo.objects.create(cliente=cliente, marca='Toyota', modelo='Corolla', placa='TEST123')
        servicio = Servicio.objects.create(nombre='Servicio Test', precio='50.00')

        orden = OrdenTrabajo.objects.create(vehiculo=vehiculo, mecanico=user, estado='pendiente')
        factura = Factura.objects.create(orden=orden, total='150.00', estado_pago='pendiente')
        pago = Pago.objects.create(factura=factura, metodo_pago='efectivo', monto='150.00')

        self.assertEqual(Cliente.objects.count(), 1)
        self.assertEqual(Vehiculo.objects.count(), 1)
        self.assertEqual(Servicio.objects.count(), 1)
        self.assertEqual(OrdenTrabajo.objects.count(), 1)
        self.assertEqual(Factura.objects.count(), 1)
        self.assertEqual(Pago.objects.count(), 1)
