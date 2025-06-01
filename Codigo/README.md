# 🚗 Full Paint Cars API

**Sistema integral de gestión para talleres de reparación y mantenimiento automotriz**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg?style=flat&logo=FastAPI)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat&logo=python)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg?style=flat&logo=mysql)](https://mysql.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Descripción

Full Paint Cars API (FPC) es una plataforma integral diseñada para el seguimiento y gestión de vehículos dentro de un taller de reparación y mantenimiento automotriz. Proporciona un sistema robusto de autenticación, gestión de usuarios y control de acceso basado en roles.

## ✨ Características Principales

- 🔐 **Autenticación JWT** - Sistema seguro de tokens con refresh automático
- 👥 **Gestión de Usuarios** - Control completo de perfiles y estados
- 🛡️ **Control de Roles** - Sistema granular de permisos (Admin, Empleado, Cliente)
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
│   │   └── 🆔 tipo_identificacion.py # Tipos de documento
│   ├── 📁 schemas/
│   │   ├── 📝 user.py             # Validación de datos de usuario
│   │   ├── 📝 role.py             # Validación de roles
│   │   └── 📝 auth.py             # Esquemas de autenticación
│   ├── 📁 controllers/
│   │   ├── 🔐 auth_controller.py  # Lógica de autenticación
│   │   ├── 👥 user_controller.py  # Lógica de usuarios
│   │   └── 🛡️ role_controller.py  # Lógica de roles
│   └── 📁 routes/
│       ├── 🛣️ auth_routes.py      # Endpoints de autenticación
│       ├── 🛣️ user_routes.py      # Endpoints de usuarios
│       └── 🛣️ role_routes.py      # Endpoints de roles
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

### 🔧 Opción 1: Clonar Repositorio Existente

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

### 🏗️ Opción 2: Crear Proyecto Desde Cero

#### 1. **Crear estructura del proyecto**
```bash
# Crear directorio principal
mkdir fullpaint_backend
cd fullpaint_backend

# Crear estructura de carpetas
mkdir -p app/{auth,models,schemas,controllers,routes}
touch app/__init__.py
touch app/{auth,models,schemas,controllers,routes}/__init__.py

# Crear archivos principales
touch app/main.py
touch app/config.py
touch app/database.py
touch requirements.txt
touch .env
touch .gitignore
touch README.md
```

#### 2. **Crear y activar entorno virtual**
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 3. **Instalar dependencias base**
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

#### 4. **Crear archivos de configuración básicos**

**📁 .gitignore**
```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/

# Environment variables
.env
.env.local
.env.production

# Database
*.db
*.sqlite3

# Logs
*.log
logs/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

**📁 app/config.py**
```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/FULLPAINTT"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Server
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    APP_NAME: str = "Full Paint Cars API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**📁 app/database.py**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Crear motor de base de datos
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300
)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

logger.info("🔗 Motor de base de datos creado exitosamente")
```

**📁 app/main.py (básico)**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="API para gestión de talleres automotrices",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Full Paint Cars API funcionando correctamente",
        "version": settings.VERSION,
        "status": "online"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG
    )
```

#### 6. **Desarrollo paso a paso (Solo para creación desde cero)**

Si estás creando el proyecto desde cero, necesitarás desarrollar los siguientes módulos en orden:

**🔐 1. Sistema de Autenticación**
```bash
# Crear archivos de autenticación
touch app/auth/auth_handler.py
touch app/auth/password_handler.py
```

**🗄️ 2. Modelos de Base de Datos**
```bash
# Crear modelos
touch app/models/user.py
touch app/models/role.py
touch app/models/tipo_identificacion.py
```

**📝 3. Esquemas de Validación**
```bash
# Crear esquemas Pydantic
touch app/schemas/user.py
touch app/schemas/role.py
touch app/schemas/auth.py
```

**🎮 4. Controladores**
```bash
# Crear lógica de negocio
touch app/controllers/auth_controller.py
touch app/controllers/user_controller.py
touch app/controllers/role_controller.py
```

**🛣️ 5. Rutas de la API**
```bash
# Crear endpoints
touch app/routes/auth_routes.py
touch app/routes/user_routes.py
touch app/routes/role_routes.py
```

**🧪 6. Probar la instalación básica**
```bash
# Ejecutar el servidor básico
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visita `http://localhost:8000` y deberías ver el mensaje de bienvenida.

**📚 7. Continuar desarrollo**

Para completar la funcionalidad completa, puedes:
- Consultar el código fuente en el repositorio
- Seguir la documentación de FastAPI
- Implementar cada módulo gradualmente

#### 7. **Verificar instalación completa**
```bash
# Verificar que todo funciona
python -c "import fastapi, sqlalchemy, pydantic; print('✅ Todas las dependencias principales instaladas')"

# Probar conexión a base de datos (opcional)
python -c "
from app.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print('✅ Conexión a base de datos exitosa')
"
```

### 🗄️ Configuración de Base de Datos (Ambas Opciones)

**Configurar base de datos MySQL**
```sql
CREATE DATABASE FULLPAINTT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'fullpaint_user'@'localhost' IDENTIFIED BY 'tu_password_seguro';
GRANT ALL PRIVILEGES ON FULLPAINTT.* TO 'fullpaint_user'@'localhost';
FLUSH PRIVILEGES;
```

### ⚙️ Configurar Variables de Entorno (Ambas Opciones)

**Crear archivo `.env` en la raíz del proyecto:**

```env
# 🗄️ Configuración de Base de Datos
DATABASE_URL=mysql+pymysql://fullpaint_user:tu_password_seguro@localhost:3306/FULLPAINTT

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

# 📧 Configuración de Email (opcional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=tu_email@gmail.com
SMTP_PASSWORD=tu_app_password
```

### 🚀 Ejecutar la Aplicación (Ambas Opciones)

**Para desarrollo (con recarga automática):**
```bash
# Desarrollo (con recarga automática)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📦 Requirements.txt

Aquí está el archivo `requirements.txt` completo basado en las dependencias actuales del proyecto:

```txt
# FastAPI y servidor
fastapi==0.104.1
uvicorn==0.24.0

# Base de datos
SQLAlchemy==2.0.23
PyMySQL==1.1.0

# Validación de datos
pydantic==2.5.0
pydantic-core==2.14.1
pydantic-settings==2.1.0
email-validator==2.1.0

# Seguridad y autenticación
passlib==1.7.4
bcrypt==4.3.0
python-jose==3.3.0
cryptography==41.0.7

# Utilidades
python-dotenv==1.0.0
python-multipart==0.0.6

# Dependencias de sistema
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
```

### 📋 Instalación de Dependencias

```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# O instalar solo las dependencias principales (mínimas)
pip install fastapi==0.104.1 uvicorn==0.24.0 sqlalchemy==2.0.23 pymysql==1.1.0 python-dotenv==1.0.0 pydantic[email]==2.5.0 pydantic-settings==2.1.0 passlib[bcrypt]==1.7.4 python-jose[cryptography]==3.3.0 python-multipart==0.0.6
```

## 📊 Base de Datos

### 🗂️ Estructura de Tablas

| Tabla | Descripción |
|-------|-------------|
| `usuarios` | Información completa de usuarios del sistema |
| `roles` | Roles disponibles (Administrador, Empleado, Cliente) |
| `tipos_identificacion` | Tipos de documento (CC, CE, TI, etc.) |

### 👤 Usuario Administrador por Defecto

Al iniciar la aplicación por primera vez, se crea automáticamente:

```
📧 Email: admin@fullpaint.com
🔑 Contraseña: Admin123!
⚠️ IMPORTANTE: Cambiar la contraseña después del primer login
```

## 🔗 Endpoints de la API

### 🔐 Auténticación
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

### 👥 Listar Usuarios (Admin)
```bash
curl -X GET "http://localhost:8000/users/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 🛡️ Asignar Rol
```bash
curl -X POST "http://localhost:8000/roles/assign/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rol_id": 2
  }'
```

## 🔧 Configuración de Producción

### 🐳 Docker (Recomendado)

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

## 🚧 Próximas Funcionalidades

- [ ] 🔧 **Gestión de Vehículos** - CRUD completo de vehículos
- [ ] 📋 **Sistema de Órdenes de Trabajo** - Seguimiento de reparaciones  
- [ ] 💰 **Módulo de Facturación** - Generación de facturas y cotizaciones
- [ ] 📊 **Dashboard de Analíticas** - Métricas del taller
- [ ] 📱 **Notificaciones Push** - Alertas en tiempo real
- [ ] 📧 **Sistema de Email** - Notificaciones por correo
- [ ] 🔄 **Integración con APIs externas** - Proveedores de repuestos
- [ ] 📦 **Gestión de Inventario** - Control de repuestos y herramientas
- [ ] ⏰ **Sistema de Citas** - Programación de servicios
- [ ] 📸 **Galería de Imágenes** - Antes y después de reparaciones

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

</div>
