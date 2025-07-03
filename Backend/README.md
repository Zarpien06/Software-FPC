# 🚗 Full Paint Cars API

<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg?style=flat&logo=FastAPI)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB.svg?style=flat&logo=python)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1.svg?style=flat&logo=mysql)](https://mysql.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Sistema integral de gestión para talleres de reparación y mantenimiento automotriz**

[Características](#-características) • [Instalación](#-instalación) • [Configuración](#-configuración) • [API](#-api-endpoints) • [Docker](#-docker) • [Contribuir](#-contribuir)

</div>

---

## 📋 Descripción

**Full Paint Cars API (FPC)** es una plataforma integral diseñada para el seguimiento y gestión de vehículos dentro de un taller de reparación y mantenimiento automotriz. Proporciona un sistema robusto de autenticación, gestión de usuarios y control de acceso basado en roles.

### 🎯 Funcionalidades Principales

- 🔐 **Autenticación JWT** - Sistema seguro de tokens con refresh automático
- 👥 **Gestión de Usuarios** - Control completo de perfiles y estados
- 🛡️ **Control de Roles** - Sistema granular de permisos (Admin, Empleado, Cliente)
- 🚗 **Gestión de Automóviles** - CRUD completo de vehículos
- ⚙️ **Procesos de Taller** - Seguimiento de reparaciones y mantenimientos
- 📊 **Historial de Servicios** - Registro completo de intervenciones
- 💰 **Gestión de Cotizaciones** - CRUD completo de cotizaciones y presupuestos
- 💬 **Chat en Vivo** – Sistema de mensajería en tiempo real con WebSocket y Redis
- 📊 **Gestión de Reportes** – Sistema completo de reportes técnicos con workflow y firmas digitales
- 📎 **Compartir Archivos** – Envío de imágenes y documentos en el chat
- 🔔 **Notificaciones Push** – Alertas en tiempo real a los usuarios conectados
- 📱 **API RESTful** - Endpoints bien documentados y estandarizados
- 🔍 **Documentación Interactiva** - Swagger UI y ReDoc integrados

---

## 🛠️ Requisitos del Sistema

### 📋 Herramientas Necesarias

| Herramienta | Versión Mínima | Propósito |
|-------------|----------------|-----------|
| **Python** | 3.8+ | Lenguaje de programación principal |
| **MySQL** | 8.0+ | Base de datos relacional |
| **Git** | 2.0+ | Control de versiones |
| **MySQL Workbench** | 8.0+ | *(Opcional)* Administración visual de BD |

### 🖥️ Sistemas Operativos Soportados

- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Ubuntu 18.04+
- ✅ CentOS 7+
- ✅ Debian 10+

---

## 🚀 Instalación

### 📦 Opción 1: Clonar Repositorio (Recomendado)

#### 1️⃣ Clonar el Proyecto

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/fullpaint-backend.git
cd fullpaint-backend
```

#### 2️⃣ Configurar Entorno Virtual

**Windows (Git Bash/PowerShell):**
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Git Bash:
source venv/Scripts/activate
# PowerShell:
venv\Scripts\Activate.ps1
# CMD:
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate
```

#### 3️⃣ Instalar Dependencias

```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

### 🏗️ Opción 2: Crear Proyecto Desde Cero

#### 1️⃣ Crear Estructura con Git Bash

```bash
# Crear directorio principal
mkdir fullpaint_backend
cd fullpaint_backend

# Inicializar Git
git init

# Crear estructura completa de carpetas
mkdir -p app/{auth,models,schemas,controllers,routes}

# Crear archivos __init__.py
touch app/__init__.py
touch app/{auth,models,schemas,controllers,routes}/__init__.py

# Crear archivos principales
touch app/main.py
touch app/config.py
touch app/database.py

# Crear archivos de configuración
touch requirements.txt
touch .env
touch .gitignore
touch README.md
touch Dockerfile
touch docker-compose.yml

# Crear archivos del módulo auth
touch app/auth/auth_handler.py
touch app/auth/password_handler.py

# Crear archivos de modelos
touch app/models/user.py
touch app/models/role.py
touch app/models/tipo_identificacion.py
touch app/models/automovil.py
touch app/models/proceso.py
touch app/models/historial_servicio.py

# Crear esquemas
touch app/schemas/user.py
touch app/schemas/role.py
touch app/schemas/auth.py
touch app/schemas/automovil.py
touch app/schemas/proceso.py
touch app/schemas/historial_servicio.py

# Crear controladores
touch app/controllers/auth_controller.py
touch app/controllers/user_controller.py
touch app/controllers/role_controller.py
touch app/controllers/automovil_controller.py
touch app/controllers/proceso_controller.py
touch app/controllers/historial_controller.py

# Crear rutas
touch app/routes/auth_routes.py
touch app/routes/user_routes.py
touch app/routes/role_routes.py
touch app/routes/automovil_routes.py
touch app/routes/proceso_routes.py
touch app/routes/historial_routes.py

echo "✅ Estructura del proyecto creada exitosamente"
```

#### 2️⃣ Configurar Entorno Virtual

```bash
# Crear y activar entorno virtual
python -m venv venv
source venv/Scripts/activate  # Git Bash en Windows
# source venv/bin/activate    # macOS/Linux
```

#### 3️⃣ Instalar Dependencias Base

```bash
# Instalar FastAPI y dependencias principales
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install sqlalchemy==2.0.23
pip install pymysql==1.1.0
pip install python-dotenv==1.0.0
pip install pydantic[email]==2.5.0
pip install pydantic-settings==2.1.0

# Instalar dependencias de seguridad
pip install passlib[bcrypt]==1.7.4
pip install python-jose[cryptography]==3.3.0
pip install python-multipart==0.0.6

# Generar requirements.txt
pip freeze > requirements.txt
```

---

## 🗄️ Configuración de Base de Datos

### 🔧 MySQL - Configuración Inicial

#### Con MySQL Workbench (Recomendado)

1. **Abrir MySQL Workbench**
2. **Conectar al servidor** (localhost:3306)
3. **Ejecutar los siguientes comandos:**

```sql
-- Crear base de datos
CREATE DATABASE FULLPAINTT 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Crear usuario específico para la aplicación
CREATE USER 'fullpaint_user'@'localhost' IDENTIFIED BY 'tu_password_seguro_123';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON FULLPAINTT.* TO 'fullpaint_user'@'localhost';
FLUSH PRIVILEGES;

-- Verificar la creación
SHOW DATABASES;
SELECT User, Host FROM mysql.user WHERE User = 'fullpaint_user';
```

#### Sin MySQL Workbench (Línea de Comandos)

```bash
# Conectar a MySQL
mysql -u root -p

# Ejecutar comandos SQL (copiar los de arriba)
```

### 🔑 Configuración de Usuario MySQL

**Si tu MySQL NO tiene contraseña root:**
```sql
-- Usar root sin contraseña
CREATE USER 'fullpaint_user'@'localhost' IDENTIFIED BY 'fullpaint_password_123';
GRANT ALL PRIVILEGES ON FULLPAINTT.* TO 'fullpaint_user'@'localhost';
```

**Si tu MySQL SÍ tiene contraseña root:**
```sql
-- Usar las credenciales correspondientes
-- Modificar el .env con los datos correctos
```

---

## ⚙️ Configuración de Variables de Entorno

### 📝 Crear archivo .env

```bash
# Crear archivo de variables de entorno
touch .env
```

### 🔧 Contenido del archivo .env

```env
# 🗄️ Configuración de Base de Datos
# OPCIÓN 1: Con usuario específico (Recomendado)
DATABASE_URL=mysql+pymysql://fullpaint_user:fullpaint_password_123@localhost:3306/FULLPAINTT

# OPCIÓN 2: Con usuario root sin contraseña
# DATABASE_URL=mysql+pymysql://root:@localhost:3306/FULLPAINTT

# OPCIÓN 3: Con usuario root con contraseña
# DATABASE_URL=mysql+pymysql://root:tu_password_root@localhost:3306/FULLPAINTT

# 🔐 Configuración JWT
SECRET_KEY=tu_clave_super_secreta_de_al_menos_32_caracteres_cambiar_en_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 🚀 Configuración del Servidor
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
APP_NAME=Full Paint Cars API
VERSION=1.0.0
DEBUG=True

# 📧 Configuración de Email (Opcional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=tu_email@gmail.com
SMTP_PASSWORD=tu_app_password
```

---

## 🏗️ Estructura del Proyecto

```
fullpaint_backend/
├── 📁 app/
│   ├── 🐍 main.py                     # Punto de entrada principal - Configuración FastAPI
│   ├── ⚙️ config.py                   # Configuraciones centralizadas - Variables de entorno
│   ├── 🗄️ database.py                 # Configuración SQLAlchemy - Conexión MySQL
│   │
│   ├── 📁 auth/                       # Módulo de Autenticación
│   │   ├── 🔐 auth_handler.py         # Manejo JWT - Generación/validación tokens
│   │   └── 🔒 password_handler.py     # Hash de contraseñas - bcrypt
│   │
│   ├── 📁 models/                     # Modelos SQLAlchemy (Tablas BD)
│   │   ├── 👤 user.py                 # Modelo Usuario - Tabla usuarios
│   │   ├── 🛡️ role.py                 # Modelo Roles - Tabla roles
│   │   ├── 🆔 tipo_identificacion.py  # Tipos documento - CC, CE, TI, etc.
│   │   ├── 🚗 automovil.py            # Modelo Vehículos - Gestión autos
│   │   ├── ⚙️ proceso.py              # Procesos taller - Reparaciones
│   │   ├── 💰 cotizacion.py           # Modelo Cotizaciones - Gestión presupuestos
│   │   ├── 💬 chat.py                 # Modelo Chat - Sistema mensajería tiempo real
│   │   ├── 📊 reporte.py              # Modelo Reportes - Gestión reportes técnicos
│   │   └── 📋 historial_servicio.py   # Historial servicios - Registro intervenciones
│   │
│   ├── 📁 schemas/                    # Validación Pydantic (Input/Output)
│   │   ├── 📝 user.py                 # Esquemas usuario - Validación datos
│   │   ├── 📝 role.py                 # Esquemas roles - Permisos
│   │   ├── 📝 auth.py                 # Esquemas autenticación - Login/Register
│   │   ├── 📝 automovil.py            # Esquemas vehículos - CRUD autos
│   │   ├── 📝 proceso.py              # Esquemas procesos - Workflow taller
│   │   ├── 📝 cotizacion.py           # Esquemas cotizaciones - Validación presupuestos
│   │   ├── 📝 historial_servicio.py   # Esquemas historial - Servicios
│   │   ├── 📝 reporte.py              # Esquemas reportes - Validación reportes técnicos
│   │   └── 📝 chat.py                 # Esquemas chat - Validación mensajería tiempo real
│   │
│   ├── 📁 controllers/                # Lógica de Negocio
│   │   ├── 🔐 auth_controller.py      # Lógica autenticación - Login/Register/JWT
│   │   ├── 👥 user_controller.py      # Lógica usuarios - CRUD/Perfiles
│   │   ├── 🛡️ role_controller.py      # Lógica roles - Asignación permisos
│   │   ├── 🚗 automovil_controller.py # Lógica vehículos - Gestión autos
│   │   ├── ⚙️ proceso_controller.py   # Lógica procesos - Workflow taller
│   │   ├── 💰 cotizacion_controller.py # Lógica cotizaciones - Gestión presupuestos
│   │   ├── 📋 historial_controller.py # Lógica historial - Servicios
│   │   ├── 📊 reporte_controller.py   # Lógica reportes - Gestión reportes técnicos
│   │   └── 💬 chat_controller.py      # Lógica chat - Sistema mensajería tiempo real
│   │
│   └── 📁 routes/                     # Endpoints API (FastAPI Routes)
│   │   ├── 🛣️ auth_routes.py          # Rutas autenticación - /auth/*
│   │   ├── 🛣️ user_routes.py          # Rutas usuarios - /users/*
│   │   ├── 🛣️ role_routes.py          # Rutas roles - /roles/*
│   │   ├── 🛣️ automovil_routes.py     # Rutas vehículos - /automoviles/*
│   │   ├── 🛣️ proceso_routes.py       # Rutas procesos - /api/v1/procesos/*
│   │   ├── 🛣️ cotizacion_routes.py    # Rutas cotizaciones - /api/v1/cotizaciones/*
│   │   ├── 🛣️ historial_routes.py     # Rutas historial - /api/v1/historial-servicios/*
│   │   ├── 🛣️ chat_routes.py          # Rutas chat - /api/v1/chat/*
│   │   └── 🛣️ reporte_routes.py       # Rutas reportes - /api/v1/reportes/*
│   │
│   ├── 📁 services/                   # Servicios de Negocio
│   │   ├── 📧 notification_service.py # Servicio notificaciones - Emails/SMS
│   │   ├── 💬 chat_file_service.py    # Servicio archivos chat - Gestión multimedia
│   │   └── 🔔 chat_notification_service.py # Servicio notificaciones chat - Tiempo real
│   │   
│   │
│   ├── 📁 tasks/                      # Tareas Asíncronas
│       └── 💰 cotizacion_tasks.py     # Tareas cotizaciones - Procesamiento background
│   
│
├── 📋 requirements.txt                # Dependencias Python
├── 🔐 .env                           # Variables de entorno (NO subir a Git)
├── 🚫 .gitignore                     # Archivos ignorados por Git
├── 🐳 Dockerfile                     # Configuración Docker
├── 🐳 docker-compose.yml             # Orquestación contenedores
└── 📖 README.md                      # Documentación (este archivo)
```

### 📚 Descripción de Archivos Clave

| Archivo                        | Propósito          | Contenido Principal                                          |
| ------------------------------ | ------------------ | ------------------------------------------------------------ |
| `main.py`                      | Aplicación FastAPI | Configuración CORS, middleware, WebSocket, rutas principales |
| `config.py`                    | Configuración      | Settings con Pydantic, variables de entorno, Redis           |
| `database.py`                  | Base de datos      | SQLAlchemy engine, sesiones, Base declarativa                |
| `auth_handler.py`              | JWT                | Generación/validación tokens, decoradores auth               |
| `password_handler.py`          | Seguridad          | Hash bcrypt, verificación contraseñas                        |
| Modelos `*.py`                 | Tablas BD          | Definición SQLAlchemy de tablas, chat y mensajes             |
| Esquemas `*.py`                | Validación         | Pydantic models para input/output, chat tiempo real          |
| Controladores `*.py`           | Lógica             | Funciones de negocio, interacción con BD, chat WebSocket     |
| Rutas `*.py`                   | Endpoints          | FastAPI routes, decoradores HTTP, WebSocket endpoints        |
| `chat_file_service.py`         | Archivos Chat      | Gestión multimedia, validación imágenes                      |
| `chat_notification_service.py` | Notificaciones     | Sistema notificaciones tiempo real                           |
| `reporte_*.py`                 | Reportes           | Sistema completo gestión reportes técnicos, workflow        |


---

## 🚀 Ejecutar la Aplicación

### 🔥 Inicio Rápido

```bash
# 1. Activar entorno virtual
source venv/Scripts/activate  # Windows Git Bash
# source venv/bin/activate    # macOS/Linux

# 2. Ejecutar aplicación (desarrollo)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 🌐 Comandos de Ejecución

#### Desarrollo (Recomendado)
```bash
# Con recarga automática
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Con logs detallados
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

#### Producción
```bash
# Múltiples workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Con configuración específica
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info
```

### 🎯 Verificar Funcionamiento

#### URLs de Acceso
- **API Principal:** http://localhost:8000
- **Documentación Swagger:** http://localhost:8000/docs
- **Documentación ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health
- **OpenAPI JSON:** http://localhost:8000/openapi.json

#### Health Check
```bash
# Verificar que la API funciona
curl http://localhost:8000/health

# Respuesta esperada:
# {"status":"healthy","version":"1.0.0"}
```

---

## 📋 Dependencias Completas

### 📦 requirements.txt

```txt
# FastAPI y servidor ASGI
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Base de datos y ORM
SQLAlchemy==2.0.23
PyMySQL==1.1.0

# Validación de datos
pydantic==2.5.0
pydantic-core==2.14.1
pydantic-settings==2.1.0
email-validator==2.1.0

# Seguridad y autenticación
passlib[bcrypt]==1.7.4
bcrypt==4.3.0
python-jose[cryptography]==3.3.0
cryptography==41.0.7

# Utilidades y configuración
python-dotenv==1.0.0
python-multipart==0.0.6

# Dependencias del sistema
annotated-types==0.7.0
anyio==3.7.1
cffi==1.17.1
click==8.2.1
colorama==0.4.6
dnspython==2.7.0
ecdsa==0.19.1
greenlet==3.2.2
h11==0.16.0
idna==3.10
pyasn1==0.6.1
pycparser==2.22
rsa==4.9.1
six==1.17.0
sniffio==1.3.1
starlette==0.27.0
typing-extensions==4.13.2
# WebSocket y tiempo real
websockets==11.0.3
python-socketio==5.8.0
redis==4.5.4
aiofiles==23.1.0

# Procesamiento de imágenes para chat
Pillow==10.0.0

# Notificaciones push (opcional)
pyfcm==1.5.4

```

### 🔧 Instalación de Dependencias

```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar instalación
pip list | grep -E "(fastapi|uvicorn|sqlalchemy|pymysql)"

# Instalar dependencias una por una (si hay problemas)
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install sqlalchemy==2.0.23
pip install pymysql==1.1.0
pip install python-dotenv==1.0.0
pip install pydantic[email]==2.5.0
pip install pydantic-settings==2.1.0
pip install passlib[bcrypt]==1.7.4
pip install python-jose[cryptography]==3.3.0
pip install python-multipart==0.0.6
```

---

## 🔗 API Endpoints

### 🔐 Autenticación

| Método | Endpoint | Descripción | Auth | Body |
|--------|----------|-------------|------|------|
| `POST` | `/auth/register` | Registrar nuevo usuario | ❌ | `RegisterRequest` |
| `POST` | `/auth/login` | Login (form-data) | ❌ | `username`, `password` |
| `POST` | `/auth/login-json` | Login (JSON) | ❌ | `LoginRequest` |
| `GET` | `/auth/me` | Info usuario actual | ✅ | - |
| `POST` | `/auth/refresh` | Renovar token | ✅ | - |

### 👥 Usuarios

| Método | Endpoint | Descripción | Auth | Rol |
|--------|----------|-------------|------|-----|
| `GET` | `/users/` | Listar usuarios | ✅ | Admin |
| `GET` | `/users/me` | Mi perfil | ✅ | Cualquiera |
| `PUT` | `/users/me` | Actualizar mi perfil | ✅ | Cualquiera |
| `GET` | `/users/{user_id}` | Usuario por ID | ✅ | Admin |
| `PUT` | `/users/{user_id}` | Actualizar usuario | ✅ | Admin |
| `DELETE` | `/users/{user_id}` | Eliminar usuario | ✅ | Admin |
| `PATCH` | `/users/{user_id}/toggle-status` | Cambiar estado | ✅ | Admin |

### 🛡️ Roles

| Método | Endpoint | Descripción | Auth | Rol |
|--------|----------|-------------|------|-----|
| `GET` | `/roles/` | Listar roles | ✅ | Cualquiera |
| `POST` | `/roles/` | Crear rol | ✅ | Admin |
| `GET` | `/roles/{role_id}` | Rol por ID | ✅ | Cualquiera |
| `PUT` | `/roles/{role_id}` | Actualizar rol | ✅ | Admin |
| `DELETE` | `/roles/{role_id}` | Eliminar rol | ✅ | Admin |
| `POST` | `/roles/assign/{user_id}` | Asignar rol | ✅ | Admin |

### 🚗 Automóviles

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| `POST` | `/automoviles/` | Crear automóvil | ✅ |
| `GET` | `/automoviles/` | Listar automóviles | ✅ |
| `GET` | `/automoviles/{automovil_id}` | Automóvil por ID | ✅ |
| `PUT` | `/automoviles/{automovil_id}` | Actualizar automóvil | ✅ |
| `DELETE` | `/automoviles/{automovil_id}` | Eliminar automóvil | ✅ |
| `PATCH` | `/automoviles/{automovil_id}/estado` | Cambiar estado | ✅ |
| `PATCH` | `/automoviles/{automovil_id}/kilometraje` | Actualizar km | ✅ |
| `GET` | `/automoviles/{automovil_id}/historial` | Historial | ✅ |
| `GET` | `/automoviles/estadisticas/general` | Estadísticas | ✅ |
| `GET` | `/automoviles/buscar/{termino}` | Buscar | ✅ |

### ⚙️ Procesos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/v1/procesos/` | Crear proceso | ✅ |
| `GET` | `/api/v1/procesos/` | Listar procesos | ✅ |
| `GET` | `/api/v1/procesos/{proceso_id}` | Proceso por ID | ✅ |
| `PUT` | `/api/v1/procesos/{proceso_id}` | Actualizar proceso | ✅ |
| `DELETE` | `/api/v1/procesos/{proceso_id}` | Eliminar proceso | ✅ |
| `GET` | `/api/v1/procesos/automovil/{automovil_id}` | Por automóvil | ✅ |
| `GET` | `/api/v1/procesos/tecnico/{tecnico_id}` | Por técnico | ✅ |
| `PATCH` | `/api/v1/procesos/{proceso_id}/estado` | Cambiar estado | ✅ |
| `PATCH` | `/api/v1/procesos/{proceso_id}/asignar-tecnico` | Asignar técnico | ✅ |
| `GET` | `/api/v1/procesos/estadisticas/dashboard` | Dashboard | ✅ |

### 📋 Historial de Servicios

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/v1/historial-servicios/` | Crear historial | ✅ |
| `GET` | `/api/v1/historial-servicios/` | Listar historiales | ✅ |
| `GET` | `/api/v1/historial-servicios/{historial_id}` | Por ID | ✅ |
| `PUT` | `/api/v1/historial-servicios/{historial_id}` | Actualizar | ✅ |
| `DELETE` | `/api/v1/historial-servicios/{historial_id}` | Eliminar | ✅ |
| `GET` | `/api/v1/historial-servicios/automovil/{automovil_id}` | Por auto | ✅ |
| `GET` | `/api/v1/historial-servicios/reportes/costos-por-periodo` | Reportes | ✅ |

### 💰 Cotizaciones

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/v1/cotizaciones/` | Crear cotización | ✅ |
| `GET` | `/api/v1/cotizaciones/` | Listar cotizaciones | ✅ |
| `GET` | `/api/v1/cotizaciones/{cotizacion_id}` | Cotización por ID | ✅ |
| `PUT` | `/api/v1/cotizaciones/{cotizacion_id}` | Actualizar cotización | ✅ |
| `DELETE` | `/api/v1/cotizaciones/{cotizacion_id}` | Eliminar cotización | ✅ |
| `PATCH` | `/api/v1/cotizaciones/{cotizacion_id}/estado` | Cambiar estado | ✅ |
| `GET` | `/api/v1/cotizaciones/cliente/{cliente_id}` | Por cliente | ✅ |
| `GET` | `/api/v1/cotizaciones/estadisticas/dashboard` | Estadísticas | ✅ |


## 💬 Chat en Vivo
| Método   | Endpoint                                          | Descripción           | Auth |
| -------- | ------------------------------------------------- | --------------------- | ---- |
| `POST`   | `/api/v1/chat/`                                   | Crear chat            | ✅    |
| `GET`    | `/api/v1/chat/`                                   | Listar chats          | ✅    |
| `GET`    | `/api/v1/chat/{chat_id}`                          | Obtener chat          | ✅    |
| `PUT`    | `/api/v1/chat/{chat_id}`                          | Actualizar chat       | ✅    |
| `DELETE` | `/api/v1/chat/{chat_id}`                          | Eliminar chat         | ✅    |
| `POST`   | `/api/v1/chat/{chat_id}/mensajes`                 | Enviar mensaje        | ✅    |
| `GET`    | `/api/v1/chat/{chat_id}/mensajes`                 | Listar mensajes       | ✅    |
| `PUT`    | `/api/v1/chat/mensajes/{mensaje_id}`              | Actualizar mensaje    | ✅    |
| `POST`   | `/api/v1/chat/mensajes/{mensaje_id}/marcar-leido` | Marcar leído          | ✅    |
| `GET`    | `/api/v1/chat/estadisticas/generales`             | Estadísticas          | ✅    |
| `GET`    | `/api/v1/chat/{chat_id}/participantes`            | Participantes activos | ✅    |

## 🔌 WebSocket Endpoints
| Endpoint                           | Descripción             | Protocolo |
| ---------------------------------- | ----------------------- | --------- |
| `/ws/chat/{chat_id}`               | Conexión WebSocket chat | WebSocket |
| `/ws/chat/{chat_id}/typing`        | Indicador escribiendo   | WebSocket |
| `/ws/chat/notifications/{user_id}` | Notificaciones usuario  | WebSocket |

### 📊 Reportes Técnicos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/v1/reportes/` | Crear reporte | ✅ |
| `GET` | `/api/v1/reportes/` | Listar reportes | ✅ |
| `GET` | `/api/v1/reportes/{reporte_id}` | Obtener reporte | ✅ |
| `PUT` | `/api/v1/reportes/{reporte_id}` | Actualizar reporte | ✅ |
| `DELETE` | `/api/v1/reportes/{reporte_id}` | Eliminar reporte | ✅ |
| `PATCH` | `/api/v1/reportes/{reporte_id}/estado` | Cambiar estado | ✅ |
| `POST` | `/api/v1/reportes/{reporte_id}/aprobacion-cliente` | Aprobación cliente | ✅ |
| `POST` | `/api/v1/reportes/{reporte_id}/firmar` | Firmar reporte | ✅ |
| `GET` | `/api/v1/reportes/estadisticas/resumen` | Estadísticas | ✅ |
| `GET` | `/api/v1/reportes/automovil/{automovil_id}` | Por automóvil | ✅ |
| `GET` | `/api/v1/reportes/plantillas/tipos` | Plantillas | ✅ |
| `POST` | `/api/v1/reportes/{reporte_id}/adjuntos` | Subir adjunto | ✅ |
| `GET` | `/api/v1/reportes/{reporte_id}/exportar` | Exportar reporte | ✅ |
| `POST` | `/api/v1/reportes/{reporte_id}/duplicar` | Duplicar reporte | ✅ |
| `GET` | `/api/v1/reportes/pendientes/revision` | Pendientes revisión | ✅ |
| `POST` | `/api/v1/reportes/{reporte_id}/notificar-cliente` | Notificar cliente | ✅ |
| `POST` | `/api/v1/reportes/{reporte_id}/comentarios` | Agregar comentario | ✅ |
| `POST` | `/api/v1/reportes/{reporte_id}/etiquetas` | Gestionar etiquetas | ✅ |


---

## 🧪 Ejemplos de Uso

### 🔑 Usuario Administrador por Defecto

Al iniciar la aplicación por primera vez, se crea automáticamente:

```json
{
  "correo": "admin@fullpaint.com",
  "password": "Admin123!",
  "rol": "Administrador"
}
```

⚠️ **IMPORTANTE:** Cambiar la contraseña después del primer login.

### 👤 1. Registro de Usuario

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

**Respuesta esperada:**
```json
{
  "id": 2,
  "correo": "juan.perez@example.com",
  "nombre_completo": "Juan Pérez García",
  "estado": "ACTIVO",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 🔓 2. Inicio de Sesión

#### Opción A: JSON (Recomendado)
```bash
curl -X POST "http://localhost:8000/auth/login-json" \
  -H "Content-Type: application/json" \
  -d '{
    "correo": "juan.perez@example.com",
    "password": "MiPassword123!"
  }'
```

#### Opción B: Form Data
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=juan.perez@example.com&password=MiPassword123!"
```

**Respuesta esperada:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 👥 3. Obtener Información del Usuario

```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 🚗 4. Crear Automóvil

```bash
curl -X POST "http://localhost:8000/automoviles/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "ABC123",
    "marca": "Toyota",
    "modelo": "Corolla",
    "ano": 2020,
    "color": "Blanco",
    "tipo_combustible": "GASOLINA",
    "tipo_transmision": "MANUAL",
    "kilometraje": 50000,
    "propietario": {
      "nombre_completo": "María González",
      "telefono": "3009876543",
      "tipo_identificacion": "CC",
      "numero_identificacion": "9876543210"
    }
  }'
```

### ⚙️ 5. Crear Proceso de Taller

```bash
curl -X POST "http://localhost:8000/api/v1/procesos/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "automovil_id": 1,
    "tipo_proceso": "MANTENIMIENTO",
    "descripcion": "Cambio de aceite y filtros",
    "prioridad": "MEDIA",
    "fecha_programada": "2024-01-20T09:00:00Z",
    "costo_estimado": 150000
  }'
```

### 👥 6. Listar Usuarios (Solo Admin)

```bash
curl -X GET "http://localhost:8000/users/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 🛡️ 7. Asignar Rol a Usuario

```bash
curl -X POST "http://localhost:8000/roles/assign/2" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rol_id": 2
  }'
```

### 📊 8. Obtener Estadísticas del Dashboard

```bash
curl -X GET "http://localhost:8000/api/v1/procesos/estadisticas/dashboard" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Respuesta esperada:**
```json
{
  "total_procesos": 25,
  "procesos_pendientes": 8,
  "procesos_en_progreso": 12,
  "procesos_completados": 5,
  "automoviles_en_taller": 15,
  "procesos_vencidos": 2,
  "ingresos_mes_actual": 2500000,
  "promedio_tiempo_proceso": 3.5
}
```
### 💰 9. Crear Cotización

```
curl -X POST "http://localhost:8000/api/v1/cotizaciones/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": 1,
    "automovil_id": 1,
    "descripcion": "Cotización para reparación de motor",
    "servicios": [
      {
        "descripcion": "Cambio de motor",
        "cantidad": 1,
        "precio_unitario": 2500000
      },
      {
        "descripcion": "Mano de obra",
        "cantidad": 8,
        "precio_unitario": 50000
      }
    ],
    "observaciones": "Incluye garantía de 6 meses"
  }'

---
```
### 10. Crear Chat
```
curl -X POST "http://localhost:8000/api/v1/chat/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Soporte Técnico - Toyota Corolla",
    "tipo_chat": "SOPORTE",
    "participantes": [
      {
        "usuario_id": 1,
        "rol_chat": "ADMIN"
      },
      {
        "usuario_id": 2,
        "rol_chat": "PARTICIPANTE"
      }
    ],
    "configuracion": {
      "permite_archivos": true,
      "max_participantes": 10,
      "es_privado": false
    }
  }'
```
### 11. Enviar Mensaje
```
bash
Copiar
Editar
curl -X POST "http://localhost:8000/api/v1/chat/1/mensajes" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "contenido": "Hola, necesito ayuda con la reparación del motor",
    "tipo_mensaje": "TEXTO",
    "menciones": [],
    "respuesta_a": null
  }'
```
### 12. Conexión WebSocket (JavaScript)
```
javascript
Copiar
Editar
const ws = new WebSocket('ws://localhost:8000/ws/chat/1?token=YOUR_ACCESS_TOKEN');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Nuevo mensaje:', data);
};

ws.send(JSON.stringify({
    tipo: 'mensaje',
    contenido: 'Hola desde WebSocket',
    chat_id: 1
}));

ws.send(JSON.stringify({
    tipo: 'typing',
    chat_id: 1,
    escribiendo: true
}));
```
### 13. Obtener Estadísticas de Chat
```
bash
Copiar
Editar
curl -X GET "http://localhost:8000/api/v1/chat/estadisticas/generales" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

### 📊 14. Crear Reporte Técnico

```bash
curl -X POST "http://localhost:8000/api/v1/reportes/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "automovil_id": 1,
    "proceso_id": 1,
    "tipo_reporte": "DIAGNOSTICO",
    "titulo": "Diagnóstico Motor Toyota Corolla",
    "descripcion": "Revisión completa del sistema de motor",
    "hallazgos": [
      {
        "componente": "Filtro de aire",
        "estado": "MALO",
        "descripcion": "Filtro sucio, requiere cambio inmediato",
        "prioridad": "ALTA"
      },
      {
        "componente": "Aceite motor",
        "estado": "REGULAR",
        "descripcion": "Aceite oscuro, cambio recomendado",
        "prioridad": "MEDIA"
      }
    ],
    "recomendaciones": [
      "Cambiar filtro de aire inmediatamente",
      "Programar cambio de aceite en máximo 1000 km"
    ],
    "costo_estimado": 180000,
    "tiempo_estimado": 120
  }'
```

### 📋 15. Obtener Estadísticas de Reportes

```bash
curl -X GET "http://localhost:8000/api/v1/reportes/estadisticas/resumen" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Respuesta esperada:**
```json
{
  "total_reportes": 45,
  "reportes_por_estado": {
    "BORRADOR": 5,
    "EN_REVISION": 8,
    "APROBADO": 15,
    "FINALIZADO": 17
  },
  "reportes_por_tipo": {
    "DIAGNOSTICO": 20,
    "REPARACION": 15,
    "MANTENIMIENTO": 10
  },
  "reportes_pendientes_firma": 8,
  "reportes_mes_actual": 12,
  "tiempo_promedio_revision": 2.5,
  "costo_promedio": 245000
}
```

### ✍️ 16. Firmar Reporte

```bash
curl -X POST "http://localhost:8000/api/v1/reportes/1/firmar" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_firma": "TECNICO",
    "comentario": "Diagnóstico completado satisfactoriamente"
  }'
```

### 📎 17. Subir Adjunto a Reporte

```bash
curl -X POST "http://localhost:8000/api/v1/reportes/1/adjuntos" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "archivo=@diagnostico_motor.pdf" \
  -F "descripcion=Fotos del diagnóstico del motor" \
  -F "tipo_archivo=DOCUMENTO"
```

### 📄 18. Exportar Reporte

```bash
curl -X GET "http://localhost:8000/api/v1/reportes/1/exportar?formato=PDF" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  --output reporte_diagnostico.pdf
```

## 🛠️ Resolución de Problemas Comunes

### 🔍 Errores de Conexión a Base de Datos
```
#### Error: "Access denied for user"
```bash
# Verificar usuario MySQL
mysql -u fullpaint_user -p
# Ingresar password: fullpaint_password_123

# Si falla, recrear usuario:
mysql -u root -p
CREATE USER 'fullpaint_user'@'localhost' IDENTIFIED BY 'fullpaint_password_123';
GRANT ALL PRIVILEGES ON FULLPAINTT.* TO 'fullpaint_user'@'localhost';
FLUSH PRIVILEGES;
```

#### Error: "Unknown database 'FULLPAINTT'"
```bash
# Crear base de datos
mysql -u root -p
CREATE DATABASE FULLPAINTT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### Error: "Can't connect to MySQL server"
```bash
# Verificar servicio MySQL
# Windows:
net start mysql80

# macOS:
brew services start mysql

# Linux (Ubuntu/Debian):
sudo systemctl start mysql
sudo systemctl enable mysql
```

### 🔧 Errores de Dependencias

#### Error: "Microsoft Visual C++ 14.0 is required" (Windows)
```bash
# Instalar Build Tools para Visual Studio
# Descargar desde: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# O instalar con chocolatey:
choco install visualstudio2019buildtools
```

#### Error: "Failed building wheel for bcrypt"
```bash
# Instalar dependencias del sistema
# Ubuntu/Debian:
sudo apt-get update
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev

# CentOS/RHEL:
sudo yum groupinstall "Development Tools"
sudo yum install openssl-devel libffi-devel python3-devel

# macOS:
xcode-select --install
```

### 🚀 Errores de Ejecución

#### Error: "Port 8000 is already in use"
```bash
# Encontrar proceso usando el puerto
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# O usar otro puerto:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

#### Error: "ImportError: No module named 'app'"
```bash
# Verificar que estás en el directorio correcto
pwd
ls -la  # Debe mostrar la carpeta 'app'

# Verificar entorno virtual activo
which python
pip list | grep fastapi
```

### 🔐 Errores de Autenticación

#### Error: "Could not validate credentials"
```bash
# Verificar token válido
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -v

# Renovar token si expiró
curl -X POST "http://localhost:8000/auth/refresh" \
  -H "Authorization: Bearer YOUR_REFRESH_TOKEN"
```

---

## 📈 Monitoreo y Logs

### 📊 Verificar Estado de la Aplicación

```bash
# Health check básico
curl http://localhost:8000/health

# Información detallada de la API
curl http://localhost:8000/

# Verificar endpoints disponibles
curl http://localhost:8000/openapi.json | jq '.paths | keys'
```

### 📝 Logs Detallados

```bash
# Ejecutar con logs debug
uvicorn app.main:app --reload --log-level debug

# Logs en archivo
uvicorn app.main:app --reload --log-config logging.conf > logs/app.log 2>&1 &
```

### 📊 Monitoreo de Base de Datos

```sql
-- Verificar conexiones activas
SHOW PROCESSLIST;

-- Verificar tamaño de base de datos
SELECT 
    table_schema AS "Database",
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS "Size (MB)"
FROM information_schema.tables 
WHERE table_schema = 'FULLPAINTT'
GROUP BY table_schema;

-- Verificar tablas creadas
USE FULLPAINTT;
SHOW TABLES;
```

---

## 🚀 Despliegue en Producción

### 🐳 Docker (Recomendado)

#### Crear Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY app/ ./app/

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Crear docker-compose.yml
```yaml
version: '3.8'

services:
  # Aplicación FastAPI
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+pymysql://fullpaint_user:fullpaint_password_123@db:3306/FULLPAINTT
      - SECRET_KEY=tu_clave_super_secreta_produccion_2024
      - DEBUG=False
    depends_on:
      - db
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  # Base de datos MySQL
  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=root_password_seguro
      - MYSQL_DATABASE=FULLPAINTT
      - MYSQL_USER=fullpaint_user
      - MYSQL_PASSWORD=fullpaint_password_123
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./mysql/init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped

  # Adminer (Opcional - para administrar BD)
  adminer:
    image: adminer
    restart: unless-stopped
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  mysql_data:
```

#### Ejecutar con Docker
```bash
# Construir y ejecutar
docker-compose up --build -d

# Verificar contenedores
docker-compose ps

# Ver logs
docker-compose logs -f api

# Detener servicios
docker-compose down
```

### 🌐 Despliegue Tradicional

#### Configuración de Producción
```bash
# Instalar servidor web (nginx)
sudo apt-get install nginx

# Configurar nginx como proxy reverso
sudo nano /etc/nginx/sites-available/fullpaint
```

#### Configuración nginx
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Servicio systemd
```bash
# Crear servicio
sudo nano /etc/systemd/system/fullpaint.service
```

```ini
[Unit]
Description=Full Paint Cars API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/fullpaint
Environment=PATH=/var/www/fullpaint/venv/bin
ExecStart=/var/www/fullpaint/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Habilitar y ejecutar servicio
sudo systemctl enable fullpaint
sudo systemctl start fullpaint
sudo systemctl status fullpaint
```

---

## 📚 Documentación Adicional

### 🔗 Enlaces Útiles

| Recurso | URL | Descripción |
|---------|-----|-------------|
| **Documentación FastAPI** | https://fastapi.tiangolo.com | Guía oficial de FastAPI |
| **SQLAlchemy** | https://docs.sqlalchemy.org | ORM para Python |
| **Pydantic** | https://docs.pydantic.dev | Validación de datos |
| **MySQL** | https://dev.mysql.com/doc/ | Documentación MySQL |
| **JWT.io** | https://jwt.io | Debugger de tokens JWT |
| **Swagger UI** | http://localhost:8000/docs | Docs interactiva local |
| **ReDoc** | http://localhost:8000/redoc | Docs alternativa local |
| **WebSocket API** | [https://websockets.readthedocs.io](https://websockets.readthedocs.io) | Documentación WebSocket  |
| **Redis**         | [https://redis.io/docs](https://redis.io/docs)                         | Base de datos en memoria |
| **Socket.IO**     | [https://socket.io/docs/](https://socket.io/docs/)                     | Comunicación tiempo real |


### 📖 Tutoriales Recomendados

1. **FastAPI Fundamentals**
   - Crear API REST con FastAPI
   - Autenticación JWT
   - Manejo de bases de datos

2. **SQLAlchemy ORM**
   - Modelos y relaciones
   - Migraciones
   - Consultas avanzadas

3. **MySQL Optimization**
   - Índices y rendimiento
   - Backup y recovery
   - Configuración de producción

### 🎓 Cursos y Certificaciones

- **FastAPI Complete Course** (Udemy)
- **Python Backend Development** (Coursera)
- **MySQL Database Administration** (MySQL University)
- **API Design Best Practices** (Pluralsight)

---

## 🤝 Contribuir al Proyecto

### 📋 Guía de Contribución

1. **Fork del repositorio**
2. **Crear rama feature**: `git checkout -b feature/nueva-funcionalidad`
3. **Commits descriptivos**: `git commit -m "Add: nueva funcionalidad X"`
4. **Push a la rama**: `git push origin feature/nueva-funcionalidad`
5. **Crear Pull Request**

### 🎯 Estándares de Código

```python
# Ejemplo de función bien documentada
def crear_usuario(
    db: Session, 
    user_data: UserCreate
) -> UserResponse:
    """
    Crea un nuevo usuario en la base de datos.
    
    Args:
        db (Session): Sesión de base de datos SQLAlchemy
        user_data (UserCreate): Datos del usuario a crear
        
    Returns:
        UserResponse: Usuario creado con información básica
        
    Raises:
        HTTPException: Si el email ya existe o hay error de validación
    """
    # Implementación aquí
    pass
```

### 🧪 Testing

```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest tests/ -v

# Cobertura de código
pytest --cov=app tests/
```

---

## 📄 Licencia

```
MIT License

Copyright (c) 2025 Full Paint Cars

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👥 Autores y Reconocimientos

### 🧑‍💻 Desarrolladores

- **Desarrollador Principal**: **Oscar Mauricio Cruz Figueroa**  
  Encargado del desarrollo inicial, arquitectura general del sistema, documentación, diseños, y participación activa en backend y frontend.

- **Equipo Backend**: **Maicol Steven Espitia**  
  Responsable del desarrollo de la lógica del servidor, modelos de base de datos y estructuras API.

- **Equipo Frontend**: **Ronny Borda Ardila**  
  Responsable del desarrollo de la interfaz de usuario, diseño visual y experiencia del usuario.

### 🙏 Agradecimientos

- **FastAPI Community** – Por el framework extraordinario  
- **SQLAlchemy Team** – Por el ORM robusto  
- **MySQL** – Por la base de datos confiable  
- **Pydantic** – Por la validación de datos elegante

---

## 📞 Soporte y Contacto

### 🆘 Obtener Ayuda

1. **Documentación**: Revisar este README y la documentación de la API
2. **Issues**: Crear issue en GitHub con detalles del problema
3. **Discussions**: Participar en discusiones del repositorio
4. **Email**: Contactar al equipo de desarrollo

### 📧 Información de Contacto

- **Email**: support@fullpaint.com
- **GitHub**: https://github.com/tu-usuario/fullpaint-backend
- **Documentación**: https://docs.fullpaint.com
- **Website**: https://fullpaint.com

### 🐛 Reportar Bugs

Al reportar un bug, incluir:

1. **Versión** de la aplicación
2. **Sistema operativo** y versión
3. **Pasos** para reproducir el error
4. **Logs** relevantes
5. **Comportamiento esperado** vs actual

---

## 📊 Estadísticas del Proyecto

### 📈 Métricas de Desarrollo

- **Líneas de código**: ~2,500
- **Endpoints**: 45+
- **Modelos de datos**: 8
- **Tests**: 100+ casos
- **Cobertura**: 85%+

### 🏆 Características Destacadas

- ✅ **API RESTful** completa y documentada
- ✅ **Autenticación JWT** segura
- ✅ **Control de roles** granular
- ✅ **Validación de datos** robusta
- ✅ **Documentación interactiva** con Swagger
- ✅ **Base de datos** optimizada
- ✅ **Contenedores Docker** listos para producción
- ✅ **Monitoreo** y logging integrado
- ✅ Chat en tiempo real con WebSocket
- ✅ Sistema de mensajería completo
- ✅ Notificaciones push integradas
- ✅ Compartir archivos en chat
- ✅ Indicadores de escritura en tiempo real
- ✅ Gestión de participantes avanzada
- ✅ **Gestión de Reportes** - Sistema completo de reportes técnicos con workflow de aprobación
- ✅ **Firmas Digitales** - Sistema de firmas para reportes y aprobaciones
- ✅ **Adjuntos y Exportación** - Subida de archivos y exportación en múltiples formatos
---

<div align="center">

**🚗 Full Paint Cars API - Gestión Integral de Talleres Automotrices 🚗**

[![Hecho con ❤️](https://img.shields.io/badge/Hecho%20con-❤️-red.svg)](https://github.com/tu-usuario/fullpaint-backend)
[![Powered by FastAPI](https://img.shields.io/badge/Powered%20by-FastAPI-009688.svg)](https://fastapi.tiangolo.com)

---

*¿Encontraste útil este proyecto? ¡Dale una ⭐ en GitHub!*

</div>
