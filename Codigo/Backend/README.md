# 🚗 Full Paint Cars API

**Sistema integral de gestión para talleres de reparación y mantenimiento automotriz**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg?style=flat&logo=FastAPI)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat&logo=python)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg?style=flat&logo=mysql)](https://mysql.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Descripción

Full Paint Cars API (FPC) es una plataforma integral diseñada para el seguimiento y gestión completa de vehículos dentro de un taller de reparación y mantenimiento automotriz. Proporciona un sistema robusto de autenticación, gestión de usuarios, control de acceso basado en roles, administración de automóviles, procesos de trabajo e historial de servicios.

## ✨ Características Principales

- 🔐 **Autenticación JWT** - Sistema seguro de tokens con refresh automático
- 👥 **Gestión de Usuarios** - Control completo de perfiles y estados
- 🛡️ **Control de Roles** - Sistema granular de permisos (Admin, Empleado, Cliente)
- 🚗 **Gestión de Automóviles** - CRUD completo de vehículos con historial
- ⚙️ **Procesos de Trabajo** - Seguimiento de servicios y reparaciones
- 📝 **Historial de Servicios** - Registro completo de mantenimientos
- 📊 **Dashboard de Estadísticas** - Métricas y reportes del taller
- 📱 **API RESTful** - Endpoints bien documentados y estandarizados
- 🔍 **Documentación Interactiva** - Swagger UI y ReDoc integrados
- 🏥 **Health Checks** - Monitoreo del estado de la aplicación
- 📊 **Logging Completo** - Trazabilidad de todas las operaciones
- 🌐 **CORS Configurado** - Listo para integraciones frontend

## 🏗️ Arquitectura del Proyecto

```
fullpaint_backend/
├── 📁 app/
│   ├── 🐍 main.py                 # Punto de entrada principal
│   ├── ⚙️ config.py               # Configuraciones centralizadas
│   ├── 🗄️ database.py             # Configuración de base de datos
│   ├── 📁 auth/
│   │   ├── 🔐 auth_handler.py     # Manejo de JWT y tokens
│   │   └── 🔒 password_handler.py # Gestión segura de contraseñas
│   ├── 📁 models/
│   │   ├── 👤 user.py             # Modelo de Usuario
│   │   ├── 🛡️ role.py             # Modelo de Roles
│   │   ├── 🚗 automovil.py        # Modelo de Automóvil
│   │   ├── ⚙️ proceso.py          # Modelo de Procesos
│   │   ├── 📝 historial_servicios.py # Modelo de Historial
│   │   └── 🆔 tipo_identificacion.py # Tipos de documento
│   ├── 📁 schemas/
│   │   ├── 📝 user.py             # Validación de datos de usuario
│   │   ├── 📝 role.py             # Validación de roles
│   │   ├── 📝 auth.py             # Esquemas de autenticación
│   │   ├── 🚗 automovil.py        # Validación de automóviles
│   │   ├── ⚙️ procesos.py         # Validación de procesos
│   │   └── 📝 historial_servicios.py # Validación de historial
│   ├── 📁 controllers/
│   │   ├── 🔐 auth_controller.py  # Lógica de autenticación
│   │   ├── 👥 user_controller.py  # Lógica de usuarios
│   │   ├── 🛡️ role_controller.py  # Lógica de roles
│   │   ├── 🚗 automovil_controller.py # Lógica de automóviles
│   │   ├── ⚙️ proceso_controller.py # Lógica de procesos
│   │   └── 📝 historial_servicios_controller.py # Lógica de historial
│   └── 📁 routes/
│       ├── 🛣️ auth_routes.py      # Endpoints de autenticación
│       ├── 🛣️ user_routes.py      # Endpoints de usuarios
│       ├── 🛣️ role_routes.py      # Endpoints de roles
│       ├── 🛣️ automovil_routes.py # Endpoints de automóviles
│       ├── 🛣️ proceso_routes.py   # Endpoints de procesos
│       └── 🛣️ historial_servicios_routes.py # Endpoints de historial
├── 📋 requirements.txt            # Dependencias del proyecto
├── 🔐 .env                        # Variables de entorno
├── 🚫 .gitignore                  # Archivos ignorados
└── 📖 README.md                   # Documentación
```

## 🚀 Instalación y Configuración

### 📋 Requisitos Previos

- Python 3.8 o superior
- MySQL 8.0 o superior
- Git (opcional, solo si clonas el repositorio)

### 🔧 Instalación Rápida

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/fullpaint-backend.git
cd fullpaint-backend
```

2. **Crear y activar entorno virtual**
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Configurar base de datos**
```sql
CREATE DATABASE FULLPAINTT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'fullpaint_user'@'localhost' IDENTIFIED BY 'tu_password_seguro';
GRANT ALL PRIVILEGES ON FULLPAINTT.* TO 'fullpaint_user'@'localhost';
FLUSH PRIVILEGES;
```

6. **Ejecutar la aplicación**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 Base de Datos

### 🗂️ Estructura de Tablas

| Tabla | Descripción |
|-------|-------------|
| `usuarios` | Información completa de usuarios del sistema |
| `roles` | Roles disponibles (Administrador, Empleado, Cliente) |
| `tipos_identificacion` | Tipos de documento (CC, CE, TI, etc.) |
| `automoviles` | Vehículos registrados en el taller |
| `procesos` | Procesos de trabajo y servicios |
| `historial_servicios` | Historial completo de servicios realizados |

### 👤 Usuario Administrador por Defecto

Al iniciar la aplicación por primera vez, se crea automáticamente:

```
📧 Email: admin@fullpaint.com
🔑 Contraseña: Admin123!
⚠️ IMPORTANTE: Cambiar la contraseña después del primer login
```

## 🔗 Endpoints de la API

### 🔐 Autenticación
| Método | Endpoint | Descripción | Auth Requerida |
|--------|----------|-------------|----------------|
| `POST` | `/auth/register` | Registrar nuevo usuario | ❌ |
| `POST` | `/auth/login` | Iniciar sesión (form-data) | ❌ |
| `POST` | `/auth/login-json` | Iniciar sesión (JSON) | ❌ |
| `GET` | `/auth/me` | Información del usuario actual | ✅ |
| `POST` | `/auth/refresh` | Renovar token de acceso | ✅ |

### 👥 Usuarios
| Método | Endpoint | Descripción | Auth Requerida |
|--------|----------|-------------|----------------|
| `GET` | `/users/` | Listar todos los usuarios | ✅ Admin |
| `GET` | `/users/me` | Mi perfil | ✅ |
| `PUT` | `/users/me` | Actualizar mi perfil | ✅ |
| `GET` | `/users/{user_id}` | Obtener usuario específico | ✅ |
| `PUT` | `/users/{user_id}` | Actualizar usuario | ✅ Admin |
| `DELETE` | `/users/{user_id}` | Eliminar usuario | ✅ Admin |
| `PATCH` | `/users/{user_id}/toggle-status` | Cambiar estado del usuario | ✅ Admin |

### 🛡️ Roles
| Método | Endpoint | Descripción | Auth Requerida |
|--------|----------|-------------|----------------|
| `GET` | `/roles/` | Listar todos los roles | ✅ |
| `POST` | `/roles/` | Crear nuevo rol | ✅ Admin |
| `GET` | `/roles/{role_id}` | Obtener rol específico | ✅ |
| `PUT` | `/roles/{role_id}` | Actualizar rol | ✅ Admin |
| `DELETE` | `/roles/{role_id}` | Eliminar rol | ✅ Admin |
| `POST` | `/roles/assign/{user_id}` | Asignar rol a usuario | ✅ Admin |

### 🚗 Automóviles
| Método | Endpoint | Descripción | Auth Requerida |
|--------|----------|-------------|----------------|
| `POST` | `/automoviles/` | Crear nuevo automóvil | ✅ |
| `GET` | `/automoviles/` | Listar automóviles | ✅ |
| `GET` | `/automoviles/{automovil_id}` | Obtener automóvil por ID | ✅ |
| `PUT` | `/automoviles/{automovil_id}` | Actualizar automóvil | ✅ |
| `DELETE` | `/automoviles/{automovil_id}` | Eliminar automóvil | ✅ Admin |
| `PATCH` | `/automoviles/{automovil_id}/estado` | Cambiar estado del automóvil | ✅ |
| `PATCH` | `/automoviles/{automovil_id}/kilometraje` | Actualizar kilometraje | ✅ |
| `GET` | `/automoviles/{automovil_id}/historial` | Obtener historial del automóvil | ✅ |
| `GET` | `/automoviles/estadisticas/general` | Obtener estadísticas generales | ✅ Admin |
| `GET` | `/automoviles/buscar/{termino}` | Buscar automóviles | ✅ |

### ⚙️ Procesos de Trabajo (RF004)
| Método | Endpoint | Descripción | Auth Requerida |
|--------|----------|-------------|----------------|
| `POST` | `/api/v1/procesos/` | Crear proceso | ✅ |
| `GET` | `/api/v1/procesos/` | Listar procesos | ✅ |
| `GET` | `/api/v1/procesos/{proceso_id}` | Obtener proceso | ✅ |
| `PUT` | `/api/v1/procesos/{proceso_id}` | Actualizar proceso | ✅ |
| `DELETE` | `/api/v1/procesos/{proceso_id}` | Eliminar proceso | ✅ Admin |
| `GET` | `/api/v1/procesos/automovil/{automovil_id}` | Procesos por automóvil | ✅ |
| `GET` | `/api/v1/procesos/tecnico/{tecnico_id}` | Procesos por técnico | ✅ |
| `PATCH` | `/api/v1/procesos/{proceso_id}/estado` | Cambiar estado del proceso | ✅ |
| `PATCH` | `/api/v1/procesos/{proceso_id}/asignar-tecnico` | Asignar técnico | ✅ |
| `PATCH` | `/api/v1/procesos/{proceso_id}/cambiar-prioridad` | Cambiar prioridad | ✅ |
| `GET` | `/api/v1/procesos/pendientes/resumen` | Resumen de pendientes | ✅ |
| `GET` | `/api/v1/procesos/estadisticas/dashboard` | Estadísticas del dashboard | ✅ |
| `GET` | `/api/v1/procesos/programados/hoy` | Procesos programados hoy | ✅ |
| `GET` | `/api/v1/procesos/vencidos/lista` | Lista de procesos vencidos | ✅ |
| `GET` | `/api/v1/procesos/reportes/productividad-tecnico/{tecnico_id}` | Reporte de productividad | ✅ |
| `GET` | `/api/v1/procesos/reportes/eficiencia-general` | Reporte de eficiencia | ✅ Admin |

### 📝 Historial de Servicios (RF004)
| Método | Endpoint | Descripción | Auth Requerida |
|--------|----------|-------------|----------------|
| `POST` | `/api/v1/historial-servicios/` | Crear historial de servicio | ✅ |
| `GET` | `/api/v1/historial-servicios/` | Listar historiales | ✅ |
| `GET` | `/api/v1/historial-servicios/{historial_id}` | Obtener historial específico | ✅ |
| `PUT` | `/api/v1/historial-servicios/{historial_id}` | Actualizar historial | ✅ |
| `DELETE` | `/api/v1/historial-servicios/{historial_id}` | Eliminar historial | ✅ Admin |
| `GET` | `/api/v1/historial-servicios/automovil/{automovil_id}` | Historial por automóvil | ✅ |
| `GET` | `/api/v1/historial-servicios/tecnico/{tecnico_id}` | Historial por técnico | ✅ |
| `GET` | `/api/v1/historial-servicios/mantenimientos/proximos` | Próximos mantenimientos | ✅ |
| `GET` | `/api/v1/historial-servicios/estadisticas/mantenimiento` | Estadísticas de mantenimiento | ✅ |
| `GET` | `/api/v1/historial-servicios/reportes/costos-por-periodo` | Reporte de costos | ✅ Admin |
| `GET` | `/api/v1/historial-servicios/reportes/eficiencia-tecnico/{tecnico_id}` | Eficiencia de técnico | ✅ |

### 🏥 Sistema
| Método | Endpoint | Descripción | Auth Requerida |
|--------|----------|-------------|----------------|
| `GET` | `/` | Información general de la API | ❌ |
| `GET` | `/health` | Verificación del estado del sistema | ❌ |

## 📖 Documentación Interactiva

Una vez ejecutada la aplicación, accede a:

- **🎯 Swagger UI**: http://localhost:8000/docs
- **📚 ReDoc**: http://localhost:8000/redoc
- **🔧 OpenAPI JSON**: http://localhost:8000/openapi.json

## 🛠️ Tecnologías Utilizadas

### 🐍 Backend
- **FastAPI 0.104.1** - Framework web moderno y rápido
- **SQLAlchemy 2.0.23** - ORM avanzado para Python
- **Pydantic** - Validación de datos y serialización
- **PyMySQL 1.1.0** - Conector MySQL para Python

### 🔐 Seguridad
- **bcrypt 4.3.0** - Hash seguro de contraseñas
- **python-jose 3.3.0** - Manejo de tokens JWT
- **passlib 1.7.4** - Biblioteca de autenticación

### 🌐 Servidor
- **Uvicorn 0.24.0** - Servidor ASGI de alto rendimiento
- **python-multipart** - Manejo de formularios multipart
- **python-dotenv** - Gestión de variables de entorno

## 🧪 Ejemplos de Uso

### 👤 Registro de Usuario
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_completo": "Juan Pérez García",
    "correo": "juan.perez@example.com",
    "password": "MiPassword123!",
    "telefono": "3001234567",
    "tipo_identificacion": "CC",
    "numero_identificacion": "1234567890"
  }'
```

### 🔓 Inicio de Sesión
```bash
curl -X POST "http://localhost:8000/auth/login-json" \
  -H "Content-Type: application/json" \
  -d '{
    "correo": "juan.perez@example.com",
    "password": "MiPassword123!"
  }'
```

### 🚗 Crear Automóvil
```bash
curl -X POST "http://localhost:8000/automoviles/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "marca": "Toyota",
    "modelo": "Corolla",
    "año": 2022,
    "placa": "ABC123",
    "numero_motor": "1234567890",
    "numero_chasis": "0987654321",
    "color": "Blanco",
    "kilometraje": 15000,
    "tipo_combustible": "GASOLINA",
    "tipo_transmision": "AUTOMATICA",
    "propietario_id": 1
  }'
```

### ⚙️ Crear Proceso de Trabajo
```bash
curl -X POST "http://localhost:8000/api/v1/procesos/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "automovil_id": 1,
    "tipo_proceso": "MANTENIMIENTO",
    "descripcion": "Cambio de aceite y filtros",
    "fecha_programada": "2024-03-15T10:00:00",
    "tecnico_asignado_id": 2,
    "prioridad": "MEDIA",
    "tiempo_estimado": 120
  }'
```

### 📝 Registrar Historial de Servicio
```bash
curl -X POST "http://localhost:8000/api/v1/historial-servicios/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "automovil_id": 1,
    "proceso_id": 1,
    "tecnico_id": 2,
    "tipo_mantenimiento": "PREVENTIVO",
    "descripcion_servicio": "Cambio de aceite motor 5W-30",
    "productos_utilizados": "Aceite 5W-30, Filtro aceite, Filtro aire",
    "costo_total": 150000.00,
    "kilometraje_actual": 15500,
    "proximo_mantenimiento_km": 20000
  }'
```

## 📊 Modelos de Datos

### 🚗 Automóvil
```python
{
  "id": 1,
  "marca": "Toyota",
  "modelo": "Corolla",
  "año": 2022,
  "placa": "ABC123",
  "numero_motor": "1234567890",
  "numero_chasis": "0987654321",
  "color": "Blanco",
  "kilometraje": 15000,
  "tipo_combustible": "GASOLINA",
  "tipo_transmision": "AUTOMATICA",
  "estado": "ACTIVO",
  "propietario_id": 1,
  "fecha_registro": "2024-01-15T10:30:00"
}
```

### ⚙️ Proceso
```python
{
  "id": 1,
  "automovil_id": 1,
  "tipo_proceso": "MANTENIMIENTO",
  "descripcion": "Cambio de aceite y filtros",
  "estado": "PENDIENTE",
  "fecha_creacion": "2024-01-15T08:00:00",
  "fecha_programada": "2024-01-15T10:00:00",
  "fecha_completado": null,
  "tecnico_asignado_id": 2,
  "prioridad": "MEDIA",
  "tiempo_estimado": 120,
  "tiempo_real": null,
  "observaciones": ""
}
```

### 📝 Historial de Servicio
```python
{
  "id": 1,
  "automovil_id": 1,
  "proceso_id": 1,
  "tecnico_id": 2,
  "fecha_servicio": "2024-01-15T11:30:00",
  "tipo_mantenimiento": "PREVENTIVO",
  "descripcion_servicio": "Cambio de aceite motor 5W-30",
  "productos_utilizados": "Aceite 5W-30, Filtro aceite",
  "costo_total": 150000.00,
  "kilometraje_actual": 15500,
  "proximo_mantenimiento_km": 20000,
  "estado": "COMPLETADO"
}
```

## 🔧 Configuración de Producción

### 🐳 Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### 🚀 Variables de Entorno para Producción

```env
DEBUG=False
SECRET_KEY=clave_super_secreta_de_produccion_de_al_menos_64_caracteres
DATABASE_URL=mysql+pymysql://user:password@db-server:3306/fullpaint_prod
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

## 📊 Monitoreo y Logs

### 📋 Health Check
```bash
curl http://localhost:8000/health
```

### 📝 Logs
Los logs se generan automáticamente en:
- **Consola**: Salida estándar con colores
- **Archivo**: `app.log` en el directorio raíz

## 🧪 Testing

### Ejecutar Tests
```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests con cobertura
pytest --cov=app

# Ejecutar tests específicos
pytest tests/test_automoviles.py
pytest tests/test_procesos.py
```

## 🤝 Contribución

1. **Fork** el proyecto
2. **Crea** una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Abre** un Pull Request

### 📝 Guías de Contribución

- Sigue las convenciones de código PEP 8
- Incluye tests para nuevas funcionalidades
- Actualiza la documentación cuando sea necesario
- Usa commits descriptivos y claros

## 🐛 Reporte de Bugs

Si encuentras un bug, por favor crea un issue con:

- **Descripción** clara del problema
- **Pasos** para reproducir el error
- **Comportamiento esperado** vs. **comportamiento actual**
- **Screenshots** si es relevante
- **Información del entorno** (OS, Python version, etc.)

## 📞 Soporte

- **📧 Email**: soporte@fullpaintcars.com
- **💬 Discord**: [Server de la Comunidad](https://discord.gg/fullpaintcars)
- **📖 Wiki**: [Documentación Técnica](https://wiki.fullpaintcars.com)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

<div align="center">

**🚗 Full Paint Cars API - Transformando la gestión de talleres automotrices**

[![GitHub stars](https://img.shields.io/github/stars/tu-usuario/fullpaint-backend.svg?style=social&label=Star)](https://github.com/tu-usuario/fullpaint-backend)
[![GitHub forks](https://img.shields.io/github/forks/tu-usuario/fullpaint-backend.svg?style=social&label=Fork)](https://github.com/tu-usuario/fullpaint-backend/fork)

*Desarrollado por Oscar Cruz, Ronny Borda, Maicol Espitia*

**Version 1.0.0** - Sistema completo de gestión automotriz

</div>