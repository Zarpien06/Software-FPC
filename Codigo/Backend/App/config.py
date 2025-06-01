import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Settings:
    # Base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/FULLPAINTT")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "tu_clave_super_secreta_aqui_cambiar_en_produccion")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Aplicación
    APP_NAME: str = os.getenv("APP_NAME", "FullPaint API")
    VERSION: str = os.getenv("VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))
    
    # Seguridad
    BCRYPT_ROUNDS: int = int(os.getenv("BCRYPT_ROUNDS", "12"))

settings = Settings()