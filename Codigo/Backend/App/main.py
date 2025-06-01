from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from sqlalchemy import text

# Importar configuración y base de datos
from app.config import settings
from app.database import engine, get_db
from app.models import user, role, tipo_identificacion

# Importar rutas
from app.routes import auth_routes, user_routes, role_routes

# Importar funciones de autenticación para crear el admin
from app.auth.password_handler import get_password_hash

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def create_default_admin():
    """
    Crea el usuario administrador por defecto si no existe
    """
    db = None
    try:
        db: Session = next(get_db())
        
        # Verificar si ya existe un rol de administrador
        admin_role = db.query(role.Role).filter(role.Role.nombre == "Administrador").first()
        if not admin_role:
            # Crear rol de administrador
            admin_role = role.Role(
                nombre="Administrador",
                descripcion="Rol con permisos completos del sistema",
                activo=True  # Asegúrate de que este campo exista en tu modelo Role
            )
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)
            logger.info("✅ Rol 'Administrador' creado exitosamente")
        
        # Verificar si ya existe un tipo de identificación por defecto
        tipo_cedula = db.query(tipo_identificacion.TipoIdentificacion).filter(
            tipo_identificacion.TipoIdentificacion.tipo_id == "CC"
        ).first()
        if not tipo_cedula:
            # Crear tipo de identificación por defecto
            tipo_cedula = tipo_identificacion.TipoIdentificacion(
                tipo_id="CC",
                descripcion="Cédula de Ciudadanía"
            )
            db.add(tipo_cedula)
            db.commit()
            db.refresh(tipo_cedula)
            logger.info("✅ Tipo de identificación 'Cédula de Ciudadanía' creado")
        
        # CORREGIDO: Usar 'correo' en lugar de 'email'
        admin_user = db.query(user.User).filter(user.User.correo == "admin@fullpaint.com").first()
        if not admin_user:
            # Crear usuario administrador por defecto
            hashed_password = get_password_hash("Admin123!")  # Contraseña por defecto
            
            # CORREGIDO: Usar los nombres de campos correctos según tu modelo User
            admin_user = user.User(
                nombre_completo="Administrador del Sistema",  # Usar nombre_completo
                correo="admin@fullpaint.com",                # Usar correo en lugar de email
                telefono="0000000000",                       # Campo telefono existe
                numero_identificacion="0000000000",          # Campo correcto
                tipo_identificacion="CC",                    # Clave foránea string
                rol_id=admin_role.id,                       # Usar rol_id
                password_hash=hashed_password            # Campo correcto          
            )
            
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            
            logger.info("🔐 Usuario administrador creado exitosamente")
            logger.info("📧 Email: admin@fullpaint.com")
            logger.info("🔑 Contraseña: Admin123!")
            logger.info("⚠️  IMPORTANTE: Cambia la contraseña después del primer login")
        else:
            logger.info("👤 Usuario administrador ya existe")
        
    except Exception as e:
        logger.error(f"❌ Error creando usuario administrador: {e}")
        if db:
            db.rollback()
        raise e
    finally:
        if db:
            db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Maneja el ciclo de vida de la aplicación
    """
    # Startup
    logger.info("=== INICIANDO FULLPAINT API ===")
    logger.info(f"🚀 {settings.APP_NAME} v{settings.VERSION} iniciado")
    logger.info(f"🔧 Modo Debug: {settings.DEBUG}")
    logger.info(f"🔐 Algoritmo JWT: {settings.ALGORITHM}")
    
    # Verificar conexión a la base de datos
    db = None
    try:
        # Crear todas las tablas (si no existen)
        user.Base.metadata.create_all(bind=engine)
        role.Base.metadata.create_all(bind=engine)
        tipo_identificacion.Base.metadata.create_all(bind=engine)
        
        # Verificar conexión
        db = next(get_db())
        db.execute(text("SELECT 1"))
        logger.info("✅ Base de datos conectada exitosamente")
        
        # Crear usuario administrador por defecto
        await create_default_admin()
        
        logger.info(f"✅ Servidor corriendo en: {settings.SERVER_HOST}:{settings.SERVER_PORT}")
        logger.info("✅ API funcionando al 100%")
        logger.info("📚 Documentación disponible en: /docs")
        logger.info("🔄 ReDoc disponible en: /redoc")
        
    except Exception as e:
        logger.error(f"❌ Error conectando a la base de datos: {e}")
        raise e
    finally:
        if db:
            db.close()
    
    yield
    
    # Shutdown
    logger.info("=== CERRANDO FULLPAINT API ===")

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="API para FPC es una plataforma integral diseñada para el seguimiento y gestión de vehículos dentro de un taller de reparación y mantenimiento automotriz.",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(role_routes.router)

# Ruta de salud
@app.get("/")
async def root():
    """
    Endpoint de verificación de estado
    """
    return {
        "message": "Full Paints Cars API funcionando correctamente",
        "version": settings.VERSION,
        "status": "online",
        "docs": "/docs",
        "admin_info": {
            "email": "admin@fullpaint.com",
            "note": "Usuario administrador disponible para primer acceso"
        }
    }

@app.get("/health")
async def health_check():
    """
    Endpoint de verificación de salud
    """
    db = None
    try:
        # Verificar conexión a la base de datos
        db = next(get_db())
        db.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "database": "connected",
            "version": settings.VERSION
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")
    finally:
        if db:
            db.close()

# Manejador de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Manejador global de excepciones
    """
    logger.error(f"Error no manejado: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
