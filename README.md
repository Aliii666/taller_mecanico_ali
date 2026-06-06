# 🔧 Backend Django — Taller Mecánico

API REST completa para gestión de un Taller Mecánico, construida con **Django 4.2** + **Django REST Framework** + **MySQL**.

---

## 📁 Estructura del Proyecto

```
taller_mecanico/
├── manage.py
├── requirements.txt
├── .env.example                  ← Copiar a .env y configurar
├── taller_mecanico/
│   ├── settings.py               ← Configuración principal
│   ├── urls.py                   ← Rutas globales
│   └── wsgi.py
└── apps/
    ├── permissions.py            ← Permisos personalizados
    ├── usuarios/                 ← Modelo de usuario + JWT
    ├── clientes/
    ├── vehiculos/
    ├── servicios/
    ├── ordenes/
    ├── facturas/
    └── pagos/
```

Cada app contiene: `models.py`, `serializers.py`, `views.py`, `urls.py`, `admin.py`

---

## ⚙️ Instalación paso a paso

### 1. Crear entorno virtual
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus datos de MySQL
```

### 4. Crear la base de datos en MySQL
```sql
CREATE DATABASE taller_mecanico_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Aplicar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario administrador
```bash
python manage.py createsuperuser
```

### 7. Iniciar el servidor
```bash
python manage.py runserver
```

API disponible en: `http://localhost:8000`
Panel admin en:   `http://localhost:8000/admin`

---

## 🗄️ Tablas y Relaciones

| Tabla            | Modelo Django  | Descripción                          |
|------------------|----------------|--------------------------------------|
| `usuarios`       | Usuario        | Extiende AbstractBaseUser + JWT      |
| `clientes`       | Cliente        | Datos del cliente                    |
| `vehiculos`      | Vehiculo       | Vehículo FK → Cliente                |
| `servicios`      | Servicio       | Catálogo de servicios                |
| `ordenes_trabajo`| OrdenTrabajo   | FK → Vehiculo + Usuario (mecánico)   |
| `facturas`       | Factura        | OneToOne → OrdenTrabajo              |
| `pagos`          | Pago           | FK → Factura                         |

---

## 🔐 Autenticación JWT

Todas las rutas (excepto login/registro) requieren el token en el header:
```
Authorization: Bearer <access_token>
```

### Rutas actuales
- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/token/refresh/`
- `GET /api/auth/me/`

Rutas antiguas compatibles:
- `POST /api/auth/registro/`
- `GET /api/auth/perfil/`
- `POST /api/auth/refresh/`

### Flujo real del backend
- `register` crea el usuario con rol `client` y también crea su perfil.
- `login` devuelve `access`, `refresh` y `user`.
- `me` devuelve el usuario autenticado completo.
- `token/refresh` renueva el access token.

### Roles
- `admin` — acceso total
- `mechanic` — acceso operativo según permisos de las vistas
- `client` — acceso básico autenticado

---

## 📡 Endpoints de la API

### 🔑 Auth
| Método | Ruta                   | Descripción              |
|--------|------------------------|--------------------------|
| POST   | `/api/auth/registro/`  | Registrar usuario        |
| POST   | `/api/auth/login/`     | Login → devuelve tokens  |
| GET    | `/api/auth/perfil/`    | Ver mi perfil            |
| POST   | `/api/auth/refresh/`   | Renovar access token     |

**Login body:**
```json
{ "email": "admin@taller.com", "password": "123456" }
```
**Respuesta:**
```json
{
  "tokens": { "access": "eyJ...", "refresh": "eyJ..." },
  "usuario": { "id": 1, "username": "admin", "role": "administrador" }
}
```

---

### 👤 Clientes — `/api/clientes/`
| Método | Ruta                   | Descripción       | Rol         |
|--------|------------------------|-------------------|-------------|
| GET    | `/api/clientes/`       | Listar            | mecánico    |
| POST   | `/api/clientes/`       | Crear             | mecánico    |
| GET    | `/api/clientes/{id}/`  | Ver uno           | mecánico    |
| PUT    | `/api/clientes/{id}/`  | Actualizar        | mecánico    |
| DELETE | `/api/clientes/{id}/`  | Eliminar          | admin       |

**Body:**
```json
{
  "nombre": "Juan Pérez",
  "telefono": "0991234567",
  "direccion": "Av. Amazonas 123",
  "correo": "juan@email.com"
}
```

---

### 🚗 Vehículos — `/api/vehiculos/`
| Método | Ruta                    | Descripción   | Rol      |
|--------|-------------------------|---------------|----------|
| GET    | `/api/vehiculos/`       | Listar        | mecánico |
| POST   | `/api/vehiculos/`       | Registrar     | mecánico |
| GET    | `/api/vehiculos/{id}/`  | Ver uno       | mecánico |
| PUT    | `/api/vehiculos/{id}/`  | Actualizar    | mecánico |
| DELETE | `/api/vehiculos/{id}/`  | Eliminar      | admin    |

**Body:**
```json
{
  "cliente": 1,
  "marca": "Toyota",
  "modelo": "Corolla",
  "placa": "ABC-1234",
  "anio": 2020
}
```

---

### 🛠️ Servicios — `/api/servicios/`
| Método | Ruta                    | Descripción   | Rol   |
|--------|-------------------------|---------------|-------|
| GET    | `/api/servicios/`       | Listar        | todos |
| POST   | `/api/servicios/`       | Crear         | admin |
| GET    | `/api/servicios/{id}/`  | Ver uno       | todos |
| PUT    | `/api/servicios/{id}/`  | Actualizar    | admin |
| DELETE | `/api/servicios/{id}/`  | Eliminar      | admin |

**Body:**
```json
{
  "nombre": "Cambio de aceite",
  "descripcion": "Aceite sintético + filtro",
  "precio": "25.00"
}
```

---

### 📋 Órdenes de Trabajo — `/api/ordenes/`
| Método | Ruta                          | Descripción        | Rol      |
|--------|-------------------------------|--------------------|----------|
| GET    | `/api/ordenes/`               | Listar             | mecánico |
| GET    | `/api/ordenes/?estado=pendiente` | Filtrar por estado | mecánico |
| POST   | `/api/ordenes/`               | Crear              | mecánico |
| GET    | `/api/ordenes/{id}/`          | Ver uno            | mecánico |
| PUT    | `/api/ordenes/{id}/estado/`   | Cambiar estado     | mecánico |
| DELETE | `/api/ordenes/{id}/`          | Eliminar           | admin    |

**Crear orden — Body:**
```json
{
  "vehiculo": 1,
  "mecanico": 2,
  "observaciones": "Ruido extraño al arrancar"
}
```

**Cambiar estado — Body:**
```json
{ "estado": "en_proceso", "observaciones": "Revisión en curso" }
```
Estados: `pendiente` | `en_proceso` | `terminado`

---

### 🧾 Facturas — `/api/facturas/`
| Método | Ruta                               | Descripción           |
|--------|------------------------------------|-----------------------|
| GET    | `/api/facturas/`                   | Listar todas          |
| GET    | `/api/facturas/?estado_pago=pendiente` | Filtrar             |
| POST   | `/api/facturas/`                   | Crear factura         |
| GET    | `/api/facturas/{id}/`              | Ver una factura       |
| PUT    | `/api/facturas/{id}/marcar-pagada/`| Marcar como pagada    |

**Body:**
```json
{ "orden": 1, "total": "125.50" }
```

---

### 💳 Pagos — `/api/pagos/`
| Método | Ruta             | Descripción         |
|--------|------------------|---------------------|
| GET    | `/api/pagos/`    | Listar pagos        |
| POST   | `/api/pagos/`    | Registrar pago      |
| GET    | `/api/pagos/{id}/` | Ver un pago       |

**Body:**
```json
{
  "factura": 1,
  "metodo_pago": "efectivo",
  "monto": "125.50"
}
```
Métodos: `efectivo` | `tarjeta` | `transferencia`

> Al registrar un pago, si el total pagado cubre el total de la factura, esta se marca automáticamente como **pagada**.

---

## 🧪 Prueba rápida con curl

```bash
# 1. Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@taller.com","password":"123456"}'

# 2. Listar clientes (usar el access token del paso anterior)
curl http://localhost:8000/api/clientes/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"

# 3. Crear cliente
curl -X POST http://localhost:8000/api/clientes/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Juan Pérez","telefono":"0991234567"}'
```

---

## 📦 Dependencias

| Paquete                          | Uso                        |
|----------------------------------|----------------------------|
| Django 4.2                       | Framework principal        |
| djangorestframework              | API REST                   |
| djangorestframework-simplejwt    | Autenticación JWT          |
| mysqlclient                      | Conector MySQL             |
| django-cors-headers              | CORS para frontend/móvil   |
| python-decouple                  | Variables de entorno .env  |
