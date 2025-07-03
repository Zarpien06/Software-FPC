from datetime import datetime, timedelta, timezone
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
import re
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db

# Configurar contexto de cifrado para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configurar OAuth2 para extraer token del header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class AuthHandler:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Crea un token JWT codificado con un tiempo de expiración.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.access_token_expire_minutes
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> dict:
        """
        Decodifica y valida un token JWT. 
        Si no es válido, lanza HTTPException 401.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_user_id_from_token(self, token: str) -> int:
        """
        Extrae el user_id del token validado.
        """
        payload = self.verify_token(token)
        user_id: Union[str, int, None] = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se pudo validar las credenciales",
                headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            return int(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="ID de usuario inválido en token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_user_role_from_token(self, token: str) -> Optional[str]:
        """
        Extrae el rol del usuario del token validado.
        """
        payload = self.verify_token(token)
        return payload.get("role")

    def create_user_token(self, user_id: int, user_email: str, user_role: str) -> str:
        """
        Genera un token JWT para un usuario con id, email y rol.
        """
        token_data = {
            "sub": str(user_id),
            "email": user_email,
            "role": user_role,
            "iat": datetime.now(timezone.utc),
        }
        return self.create_access_token(token_data)


class PasswordHandler:
    @staticmethod
    def hash_password(password: str) -> str:
        """Cifra una contraseña usando bcrypt"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica una contraseña contra su hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """Valida la fortaleza de una contraseña. Retorna (es_valida, mensaje)"""
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        if len(password) > 128:
            return False, "La contraseña no puede tener más de 128 caracteres"
        if not re.search(r"[a-z]", password):
            return False, "La contraseña debe contener al menos una letra minúscula"
        if not re.search(r"[A-Z]", password):
            return False, "La contraseña debe contener al menos una letra mayúscula"
        if not re.search(r"\d", password):
            return False, "La contraseña debe contener al menos un número"
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
            return False, "La contraseña debe contener al menos un carácter especial"
        return True, "Contraseña válida"


# Funciones auxiliares para compatibilidad
def get_password_hash(password: str) -> str:
    """Función auxiliar para hashear contraseñas - mantiene compatibilidad"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Función auxiliar para verificar contraseñas - mantiene compatibilidad"""  
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Obtiene el usuario actual a partir del token JWT.
    Lanza 401 si el token es inválido o usuario no existe.
    """
    from app.models.user import User  # Import aquí para evitar imports circulares
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.usuario_id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_admin_user(current_user = Depends(get_current_user)):
    """
    Obtiene el usuario actual y verifica que sea administrador.
    Lanza 403 si no tiene permisos de administrador.
    """
    # Verificar si el usuario tiene rol de administrador
    if not current_user.role or current_user.role.nombre.lower() not in ['admin', 'administrador']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador"
        )
    return current_user


async def get_current_active_user(current_user = Depends(get_current_user)):
    """
    Obtiene el usuario actual y verifica que esté activo.
    """
    if not current_user.is_active():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return current_user

def decode_token(token: str) -> dict:
    """
    Decodifica un token JWT y retorna el payload.
    Lanza una excepción HTTP 401 si el token es inválido.
    """
    return auth_handler.verify_token(token)

class JWTBearer(HTTPBearer):
    """
    Dependencia personalizada que extiende HTTPBearer para validar tokens JWT automáticamente.
    """
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Esquema de autenticación inválido"
                )
            if not auth_handler.verify_token(credentials.credentials):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Token inválido o expirado"
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No se proporcionó token"
            )

# Instancias globales para importar y usar en otros módulos
auth_handler = AuthHandler()
password_handler = PasswordHandler()