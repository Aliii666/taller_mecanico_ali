from django.test import TestCase
from rest_framework.test import APIClient
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


class AuthApiTest(TestCase):
    def test_register_returns_user(self):
        client = APIClient()
        response = client.post(
            '/api/auth/register/',
            {
                'username': 'nuevo',
                'email': 'nuevo@example.com',
                'password': 'secreto123',
                'password2': 'secreto123',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn('message', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], 'nuevo@example.com')
        self.assertEqual(response.data['user']['role']['name'], 'client')

    def test_login_returns_tokens_and_user(self):
        User = get_user_model()
        User.objects.create_user(username='nuevo', email='nuevo@example.com', password='secreto123')

        client = APIClient()
        response = client.post(
            '/api/auth/login/',
            {
                'email': 'nuevo@example.com',
                'password': 'secreto123',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_me_requires_token(self):
        User = get_user_model()
        user = User.objects.create_user(username='nuevo', email='nuevo@example.com', password='secreto123')

        client = APIClient()
        login_response = client.post(
            '/api/auth/login/',
            {
                'email': 'nuevo@example.com',
                'password': 'secreto123',
            },
            format='json',
        )

        client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}")
        me_response = client.get('/api/auth/me/')

        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.data['email'], user.email)
