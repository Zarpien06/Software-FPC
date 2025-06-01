from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.config import settings
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear engine de SQLAlchemy
try:
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,  # Mostrar queries SQL en desarrollo
        pool_pre_ping=True,   # Verificar conexiones antes de usar
        pool_recycle=300      # Reciclar conexiones cada 5 minutos
    )
    logger.info("🔗 Motor de base de datos creado exitosamente")
except Exception as e:
    logger.error(f"❌ Error al crear motor de base de datos: {e}")
    raise

# Crear SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Dependency para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Error en sesión de base de datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# Función para verificar conexión a la base de datos
def verify_database_connection():
    try:
        db = SessionLocal()
        # Ejecutar una query simple para verificar conexión
        db.execute("SELECT 1")
        db.close()
        logger.info("✅ Conexión a la base de datos verificada exitosamente")
        return True
    except Exception as e:
        logger.error(f"❌ Error al conectar con la base de datos: {e}")
        return False

# Función para crear todas las tablas
def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("📊 Tablas de base de datos sincronizadas")
    except Exception as e:
        logger.error(f"❌ Error al crear tablas: {e}")
        raise